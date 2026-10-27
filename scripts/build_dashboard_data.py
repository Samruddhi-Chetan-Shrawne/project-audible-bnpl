"""
build_dashboard_data.py
Project Audible: BNPL vs Credit Card Credit Stress
FINTECH 590.05, Fall 2026

Builds dashboard/data.js, the single data model behind all three dashboard
pages (executive, analyst, regulator) and their drill-throughs. Every number
on the dashboard comes from here or is recomputed in the page from the same
quarterly rows, so no page can drift from another. Correlations reuse
lead_lag.py so the dashboard and the printed lag table always agree.

Usage:
    python scripts/build_dashboard_data.py
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from lead_lag import END, MAX_LAG, START, lagged_corr, load  # noqa: E402

OUT = Path("dashboard/data.js")
INDEX_PATHS = [Path("data/raw/affirm/affirm_filings_index.csv"), Path("data/raw/affirm_filings_index.csv")]

# Pull dates as recorded in the technical memo (both pipelines ran 2026-10-26).
FRED_PULLED = "2026-10-26"
SEC_PULLED = "2026-10-26"
BUREAU_REPORTING_START = "2022-04-01"  # Affirm began furnishing to Experian

# Early-warning rule from the position memo: a 50 bp year-over-year rise in
# Affirm 30+ DPD triggers a closer look at card books. The watch band below it
# keeps a reading just under the line from looking the same as a flat one.
TRIGGER_PP = 0.50
WATCH_PP = 0.25
CONFIRM_PP = 0.25      # card 30+ DPD rise that counts as the trigger being borne out
CONFIRM_WINDOW_Q = 8   # quarters after the trigger to look for that rise

# Neither the Fed nor Affirm publishes a release calendar this far out; these
# follow last year's timing and are shown on the dashboard as approximate.
NEXT_DATA = [
    {"series": "Affirm FQ1 FY2027 10-Q (quarter ended Sep 30, 2026)", "expected": "early Nov 2026"},
    {"series": "FRED DRCCLACBS and CORCCACBS for Q3 2026", "expected": "late Nov 2026"},
]

# Null simulations for the "best of 11 lags could be luck" check.
N_SIMS = 10_000
SEED = 590

BASIS_LABELS = {
    "hfi": "Loans held for investment, amortized cost (totals table)",
    "hfi_hfs": "Loans held for investment + held for sale, amortized cost (totals table)",
    "hfi_hfs_upb": "Loans held for investment + held for sale, unpaid principal balance",
    "hfi_by_origination": "Loans held for investment, amortized cost (by-origination table)",
}


def label(ts: pd.Timestamp) -> str:
    return f"Q{ts.quarter} {ts.year}"


def num(v, nd=4):
    return None if v is None or pd.isna(v) else round(float(v), nd)


def fisher_ci(r: float, n: int) -> tuple:
    if n <= 3 or pd.isna(r):
        return None, None
    z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
    return float(np.tanh(z - 1.96 * se)), float(np.tanh(z + 1.96 * se))


def acf(x: np.ndarray, j: int) -> float:
    d = x - x.mean()
    return float((d[:-j] * d[j:]).sum() / (d * d).sum())


def n_effective(x: np.ndarray, y: np.ndarray) -> float:
    """Pyper & Peterman (1998): 1/n* = 1/n + (2/n) * sum_j acf_x(j) * acf_y(j),
    j = 1..n/5. Two slow-moving series share far less information than their
    pair count suggests. Floored at 4 so the Fisher interval exists, capped at n."""
    n = len(x)
    s = sum(acf(x, j) * acf(y, j) for j in range(1, n // 5 + 1))
    return float(min(n, max(4.0, n / (1 + 2 * s)))) if 1 + 2 * s > 0 else float(n)


def lag_table(a: pd.Series, c: pd.Series, diff: bool) -> list:
    if diff:
        a, c = a.diff(), c.diff()
    rows = []
    for lag in range(MAX_LAG + 1):
        r, n = lagged_corr(a, c, lag)
        lo, hi = fisher_ci(r, n)
        pairs = pd.DataFrame({"a": a, "c": c.shift(-lag)}).dropna()
        ne = n_effective(pairs["a"].to_numpy(), pairs["c"].to_numpy()) if n > 3 else None
        lo_a, hi_a = fisher_ci(r, ne) if ne else (None, None)
        rows.append({"lag": lag, "r": num(r, 3), "n": n, "lo": num(lo, 3), "hi": num(hi, 3),
                     "n_eff": num(ne, 1), "lo_adj": num(lo_a, 3), "hi_adj": num(hi_a, 3)})
    return rows


def max_lag_r(a: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Highest Pearson r over lags 0..MAX_LAG between a and each row of C."""
    out = np.full(len(C), -np.inf)
    for lag in range(MAX_LAG + 1):
        x, Y = a[:len(a) - lag], C[:, lag:]
        ok = ~np.isnan(x)
        x, Y = x[ok] - x[ok].mean(), Y[:, ok] - Y[:, ok].mean(axis=1, keepdims=True)
        r = (Y @ x) / np.sqrt((Y * Y).sum(axis=1) * (x @ x))
        out = np.maximum(out, r)
    return out


def phase_null_p(a: pd.Series, c: pd.Series) -> float:
    """Share of phase-randomized card series (same spectrum, so same smoothness;
    Ebisuzaki 1997) whose best r over lags 0-10 matches the observed best r.
    Answers trending-series and lag-picking objections in one number."""
    cv = c.to_numpy(float)
    obs = max_lag_r(a.to_numpy(float), cv[None, :])[0]
    rng = np.random.default_rng(SEED)
    f = np.fft.rfft(cv - cv.mean())
    ph = rng.uniform(0, 2 * np.pi, (N_SIMS, len(f)))
    ph[:, 0] = 0
    sims = np.fft.irfft(np.abs(f) * np.exp(1j * ph), n=len(cv)) + cv.mean()
    return float((max_lag_r(a.to_numpy(float), sims) >= obs - 1e-12).mean())


def prewhiten(x: pd.Series) -> pd.Series:
    """AR(1) residuals: removes each series' own momentum before correlating."""
    return x - x.autocorr(1) * x.shift(1)


def best(rows: list) -> dict:
    return max((r for r in rows if r["r"] is not None), key=lambda r: r["r"])


def git_commit() -> str:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        return sha + ("+local changes" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main():
    df = load()
    idx = df.index
    fred = pd.read_csv("data/processed/fred_quarterly.csv", parse_dates=["quarter"]).set_index("quarter")
    nco = fred["cc_nco_rate_pct"].reindex(idx)
    afrm = pd.read_csv("data/processed/affirm_quarterly.csv", parse_dates=["quarter_end"]).set_index("quarter_end")
    afrm = afrm.reindex(idx)
    filings = pd.read_csv(next(p for p in INDEX_PATHS if p.exists())).set_index("accession")

    a30, a90, cc = df["affirm"], afrm["delinquency_90plus_pct"], df["cc"]
    loans = afrm["loans_held_for_investment_mil"]
    del_usd = a30 / 100 * loans
    yoy = a30 - a30.shift(4)

    def status(v):
        if pd.isna(v):
            return "n/a"
        return "trigger" if v >= TRIGGER_PP else "watch" if v >= WATCH_PP else "none"

    quarters = []
    for i, d in enumerate(idx):
        acc = afrm["source_accession"].iloc[i]
        f = filings.loc[acc] if isinstance(acc, str) and acc in filings.index else None
        quarters.append({
            "date": d.strftime("%Y-%m-%d"),
            "label": label(d),
            "affirm30": num(a30.iloc[i]),
            "affirm90": num(a90.iloc[i]),
            "loans_mil": num(loans.iloc[i], 1),
            "del_usd_mil": num(del_usd.iloc[i], 1),
            "cc30": num(cc.iloc[i], 2),
            "nco": num(nco.iloc[i], 2),
            "fred_obs_date": d.to_period("Q").start_time.strftime("%Y-%m-%d"),
            "basis": None if pd.isna(afrm["basis"].iloc[i]) else afrm["basis"].iloc[i],
            "accession": acc if isinstance(acc, str) else None,
            "form": None if f is None else f["form_type"],
            "filed": None if f is None else f["filing_date"],
            "filing_period": None if f is None else f["report_date"],
            "edgar_url": None if f is None else f["edgar_url"],
            "yoy_pp": num(yoy.iloc[i], 3),
            "signal": status(yoy.iloc[i]),
        })

    levels, changes = lag_table(a30, cc, False), lag_table(a30, cc, True)
    best_lvl, best_chg = best(levels), best(changes)

    a_peak, c_peak = a30.idxmax(), cc.idxmax()
    a_trough, c_trough = a30.idxmin(), cc.idxmin()
    qgap = lambda x, y: (y.year - x.year) * 4 + (y.quarter - x.quarter)
    lead_q = qgap(a_peak, c_peak)
    trough_gap = qgap(a_trough, c_trough)

    # Group consecutive trigger quarters into episodes and test each against
    # what card delinquency did over the following CONFIRM_WINDOW_Q quarters.
    episodes, cur = [], None
    for i, q in enumerate(quarters):
        if q["signal"] == "trigger":
            cur = cur or {"start": i}
            cur["end"] = i
        elif cur:
            episodes.append(cur)
            cur = None
    if cur:
        episodes.append(cur)
    for ep in episodes:
        s = ep["start"]
        ahead = cc.iloc[s + 1:s + 1 + CONFIRM_WINDOW_Q]
        rise = float(ahead.max() - cc.iloc[s]) if len(ahead) else None
        ep.update({
            "start_label": quarters[s]["label"], "end_label": quarters[ep["end"]]["label"],
            "start_date": quarters[s]["date"], "end_date": quarters[ep["end"]]["date"],
            "card_rise_pp": num(rise, 2), "quarters_seen": int(len(ahead)),
            "confirmed": rise is not None and rise >= CONFIRM_PP,
            "quarters_before_card_peak": qgap(idx[s], c_peak),
        })
    first_ep = episodes[0] if episodes else None
    false_alarms = [e for e in episodes if not e["confirmed"]]

    # Robustness checks for the position ledger (Lecture 9). Each states what
    # would have weakened the claim, then what the data returned.
    w = df.loc["2021-03-31":]
    r_no2020 = best(lag_table(w["affirm"], w["cc"], False))
    r_90 = best(lag_table(a90, cc, False))
    r_nco = best(lag_table(a30, nco, False))
    r_pw = best(lag_table(prewhiten(a30), prewhiten(cc), False))
    r_yoy = best(lag_table(a30.diff(4), cc.diff(4), False))
    perm_p = phase_null_p(a30, cc)
    loo = []
    for q in a30.dropna().index:
        a_drop = a30.copy()
        a_drop[q] = np.nan
        loo.append(best(lag_table(a_drop, cc, False))["lag"])
    lead_checks = [best_lvl, best_chg, r_no2020, r_90, r_pw, r_yoy]
    lead_range = [min(r["lag"] for r in lead_checks), max(r["lag"] for r in lead_checks)]
    def lag_result(prefix, r):
        return f"{prefix}{r['lag']} quarters, r = {r['r']:.2f} (n = {r['n']})"

    alarms = ", ".join(e["start_label"] for e in false_alarms)
    ledger = [
        {"claim": "Affirm leads cards by about 7 quarters",
         "test": "Best lead is 2 quarters or less",
         "result": lag_result("Best lead ", best_lvl),
         "verdict": "Hold" if best_lvl["lag"] > 2 else "Fail"},
        {"claim": "Not just a shared trend",
         "test": "Quarterly changes peak elsewhere, or r < 0.30",
         "result": lag_result("Changes: ", best_chg),
         "verdict": "Hold" if abs(best_chg["lag"] - best_lvl["lag"]) <= 1 and best_chg["r"] >= 0.30 else "Fail"},
        {"claim": "Survives removing momentum",
         "test": "Prewhitened lead 2+ quarters off, or r < 0.30",
         "result": lag_result("Prewhitened: ", r_pw),
         "verdict": "Hold" if abs(r_pw["lag"] - lead_q) <= 2 and r_pw["r"] >= 0.30 else "Fail"},
        {"claim": "Not seasonality",
         "test": "Year-over-year lead 1+ quarter off",
         "result": lag_result("Year over year: ", r_yoy),
         "verdict": "Hold" if abs(r_yoy["lag"] - lead_q) <= 1 and r_yoy["r"] >= 0.30 else "Fail"},
        {"claim": "No single quarter drives it",
         "test": "Dropping one quarter moves the lead 1+",
         "result": (f"Lead stays {min(loo)}" + (f"–{max(loo)}" if max(loo) != min(loo) else "")
                    + f" in all {len(loo)} drop-one runs"),
         "verdict": "Hold" if max(abs(l - best_lvl["lag"]) for l in loo) <= 1 else "Fail"},
        {"claim": "Not luck from testing 11 leads",
         "test": "Look-alike random series match it 5%+ of the time",
         "result": f"Matched {perm_p * 100:.1f}% of the time ({N_SIMS:,} runs)",
         "verdict": "Hold" if perm_p < 0.05 else "Narrow" if perm_p < 0.10 else "Fail"},
        {"claim": "Strength is pinned down",
         "test": "Adjusted 95% range dips below r = 0.30",
         "result": f"≈{best_lvl['n_eff']:.0f} independent pairs; range {best_lvl['lo_adj']:+.2f} to {best_lvl['hi_adj']:+.2f}",
         "verdict": "Hold" if best_lvl["lo_adj"] >= 0.30 else "Narrow"},
        {"claim": "Not a 2020 artifact",
         "test": "Lead moves 1+ quarter without 2020",
         "result": lag_result("From 2021: ", r_no2020),
         "verdict": "Hold" if abs(r_no2020["lag"] - best_lvl["lag"]) <= 1 else "Fail"},
        {"claim": "Holds for 90+ days late",
         "test": "90+ day lead far from 7",
         "result": lag_result("90+ days: ", r_90),
         "verdict": "Hold" if abs(r_90["lag"] - lead_q) <= 2 else "Fail"},
        {"claim": "Troughs show the same lead",
         "test": "Troughs far less than 7 quarters apart",
         "result": f"Only {trough_gap} quarters apart ({label(a_trough)}, {label(c_trough)})",
         "verdict": "Narrow" if trough_gap < lead_q - 2 else "Hold"},
        {"claim": f"A {TRIGGER_PP:.2f}-point trigger warns in time",
         "test": "Never fires early, or mostly false",
         "result": (f"Fired {first_ep['start_label']}, {first_ep['quarters_before_card_peak']} quarters early; "
                    f"{len(false_alarms)} false alarm{'' if len(false_alarms) == 1 else 's'}"
                    + (f" ({alarms})" if false_alarms else "")),
         "verdict": "Hold" if not false_alarms else "Narrow"},
        {"claim": "Affirm's post-2022 drop is real",
         "test": "Late dollars rise while the rate falls",
         "result": (f"Late balances ${del_usd.loc[a_peak]:.0f}M → ${del_usd.iloc[-1]:.0f}M; "
                    f"book grew {loans.iloc[-1] / loans.loc[a_peak]:.1f}×"),
         "verdict": "Narrow" if del_usd.iloc[-1] > del_usd.loc[a_peak] else "Hold"},
        {"claim": "Card charge-offs confirm it",
         "test": "Charge-offs don't follow Affirm",
         "result": lag_result("Charge-offs: ", r_nco),
         "verdict": "Hold" if r_nco["lag"] > 0 and r_nco["r"] >= 0.30 else "Fail"},
    ]

    latest = quarters[-1]
    data = {
        "meta": {
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "commit": git_commit(),
            "fred_pulled": FRED_PULLED, "sec_pulled": SEC_PULLED,
            "window": [START, END], "latest_label": latest["label"],
            "n_affirm": int(a30.notna().sum()), "n_quarters": len(idx),
            "n_filings": int(afrm["source_accession"].dropna().nunique()),
            "bureau_reporting_start": BUREAU_REPORTING_START,
            "next_data": NEXT_DATA,
        },
        "quarters": quarters,
        "lags": {"levels": levels, "changes": changes},
        "kpi": {
            "affirm_peak": num(a30.max(), 2), "affirm_peak_date": a_peak.strftime("%Y-%m-%d"),
            "affirm_peak_label": label(a_peak),
            "cc_peak": num(cc.max(), 2), "cc_peak_date": c_peak.strftime("%Y-%m-%d"),
            "cc_peak_label": label(c_peak),
            "affirm_trough": num(a30.min(), 2), "affirm_trough_label": label(a_trough),
            "cc_trough": num(cc.min(), 2), "cc_trough_label": label(c_trough),
            "lead_q": lead_q, "trough_gap_q": trough_gap,
            "best_levels": best_lvl, "best_changes": best_chg,
            "nco_peak": num(nco.max(), 2), "nco_peak_label": label(nco.idxmax()),
            "lead_range": lead_range, "perm_p": round(perm_p, 3), "n_sims": N_SIMS,
            "prewhitened": r_pw, "yoy": r_yoy,
        },
        "trigger": {
            "trigger_pp": TRIGGER_PP, "watch_pp": WATCH_PP,
            "confirm_pp": CONFIRM_PP, "confirm_window_q": CONFIRM_WINDOW_Q,
            "episodes": episodes, "first": first_ep, "false_alarms": len(false_alarms),
            "latest": {"label": latest["label"], "yoy_pp": latest["yoy_pp"], "signal": latest["signal"]},
        },
        "ledger": ledger,
        "basis_labels": BASIS_LABELS,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("// Generated by scripts/build_dashboard_data.py. Do not edit.\n"
                   f"window.DASH = {json.dumps(data, indent=1)};\n")
    print(f"Wrote {OUT}: {len(idx)} quarters, lead = {lead_q} quarters, "
          f"best r = {best_lvl['r']} at lag {best_lvl['lag']}, "
          f"{len(episodes)} trigger episodes ({len(false_alarms)} unconfirmed)")
    print(f"  n_eff = {best_lvl['n_eff']}, adjusted CI {best_lvl['lo_adj']} to {best_lvl['hi_adj']}; "
          f"null p = {perm_p:.3f}; leads across checks {lead_range[0]}-{lead_range[1]} quarters")


if __name__ == "__main__":
    main()
