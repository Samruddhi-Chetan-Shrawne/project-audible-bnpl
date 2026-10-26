"""
lead_lag.py
Project Audible: BNPL vs Credit Card Credit Stress
FINTECH 590.05, Fall 2026

Pearson correlation between Affirm 30+ DPD and credit card 30+ DPD (FRED
DRCCLACBS) at lags 0-10 quarters, where lag N pairs Affirm at quarter t with
cards at quarter t+N (Affirm leads cards by N quarters). Quarters missing from
either series are dropped pairwise, so n shrinks as the lag grows.

Also reports the same correlation on quarter-over-quarter changes, as a check
that a levels correlation isn't just two series sharing a slow trend.

Usage:
    python lead_lag.py
"""

import pandas as pd

START, END = "2020-06-30", "2026-06-30"
MAX_LAG = 10


def load() -> pd.DataFrame:
    fred = pd.read_csv("data/processed/fred_quarterly.csv", parse_dates=["quarter"])
    cc = fred.set_index("quarter")["cc_30plus_dpd_rate_pct"].loc[START:END]
    afrm = pd.read_csv("data/processed/affirm_quarterly.csv", parse_dates=["quarter_end"])
    affirm = afrm.set_index("quarter_end")["delinquency_30plus_pct"]
    # Full quarterly grid; Affirm has no 2020 Q3 filing, which stays NaN.
    return pd.DataFrame({"affirm": affirm.reindex(cc.index), "cc": cc})


def lagged_corr(a: pd.Series, c: pd.Series, lag: int) -> tuple[float, int]:
    pairs = pd.DataFrame({"a": a, "c": c.shift(-lag)}).dropna()
    return pairs["a"].corr(pairs["c"]), len(pairs)


def main():
    df = load()
    rows = []
    for lag in range(MAX_LAG + 1):
        r_lvl, n_lvl = lagged_corr(df["affirm"], df["cc"], lag)
        r_chg, n_chg = lagged_corr(df["affirm"].diff(), df["cc"].diff(), lag)
        rows.append({"lag_q": lag, "r_levels": r_lvl, "n_levels": n_lvl,
                     "r_changes": r_chg, "n_changes": n_chg})
    out = pd.DataFrame(rows)
    print(out.to_string(index=False, float_format=lambda v: f"{v:+.3f}"))

    best = out.loc[out["r_levels"].idxmax()]
    best_chg = out.loc[out["r_changes"].idxmax()]
    print(f"\nLevels:  max r = {best['r_levels']:+.3f} at lag {int(best['lag_q'])} "
          f"(n = {int(best['n_levels'])})")
    print(f"Changes: max r = {best_chg['r_changes']:+.3f} at lag {int(best_chg['lag_q'])} "
          f"(n = {int(best_chg['n_changes'])})")


if __name__ == "__main__":
    main()
