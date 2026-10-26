"""
chart_lead_lag.py
Project Audible: BNPL vs Credit Card Credit Stress
FINTECH 590.05, Fall 2026

Validation chart: Affirm's 30+ DPD rate vs the FRED credit card 30+ DPD rate
(DRCCLACBS), 2020 Q2 to 2026 Q2, with each series' peak annotated. Prints the
peak quarter and value for each series and the number of quarters between them.

Usage:
    python chart_lead_lag.py

Inputs:
    data/processed/fred_quarterly.csv
    data/processed/affirm_quarterly.csv
Output:
    outputs/chart_lead_lag.png
"""

from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

START, END = "2020-06-30", "2026-06-30"
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Categorical slots 1-2 of the dataviz reference palette (light mode).
AFFIRM_COLOR = "#2a78d6"
CC_COLOR     = "#eb6834"
TEXT         = "#0b0b0b"
TEXT_MUTED   = "#52514e"
GRID         = "#e4e3df"
SURFACE      = "#fcfcfb"


def load() -> tuple[pd.Series, pd.Series]:
    fred = pd.read_csv("data/processed/fred_quarterly.csv", parse_dates=["quarter"])
    cc = fred.set_index("quarter")["cc_30plus_dpd_rate_pct"].loc[START:END]
    afrm = pd.read_csv("data/processed/affirm_quarterly.csv", parse_dates=["quarter_end"])
    affirm = afrm.set_index("quarter_end")["delinquency_30plus_pct"].sort_index().loc[START:END]
    # Align to the full quarterly grid so missing quarters break the line.
    return affirm.reindex(cc.index), cc


def peak(s: pd.Series) -> tuple[pd.Timestamp, float]:
    return s.idxmax(), s.max()


def quarter_label(ts: pd.Timestamp) -> str:
    return f"{ts.year} Q{ts.quarter}"


def main():
    affirm, cc = load()
    a_q, a_v = peak(affirm)
    c_q, c_v = peak(cc)
    lag = (c_q.to_period("Q") - a_q.to_period("Q")).n

    print(f"Affirm peak:      {quarter_label(a_q)} ({a_q.date()}) at {a_v:.2f}%")
    print(f"Credit card peak: {quarter_label(c_q)} ({c_q.date()}) at {c_v:.2f}%")
    print(f"Quarters between peaks: {lag} ({lag / 4:.2f} years)")

    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ax.plot(affirm.index, affirm.values, color=AFFIRM_COLOR, lw=2,
            marker="o", ms=4, label="Affirm (10-K/10-Q aging tables)")
    ax.plot(cc.index, cc.values, color=CC_COLOR, lw=2,
            marker="o", ms=4, label="Credit cards, all commercial banks (FRED DRCCLACBS)")

    # Peak markers get a surface ring so they read on top of the line.
    for q, v, color, text, offset in [
        (a_q, a_v, AFFIRM_COLOR, f"Affirm peak\n{quarter_label(a_q)}: {a_v:.2f}%", (-70, 18)),
        (c_q, c_v, CC_COLOR, f"Credit card peak\n{quarter_label(c_q)}: {c_v:.2f}%", (10, 30)),
    ]:
        ax.plot(q, v, "o", ms=9, color=color, mec=SURFACE, mew=2, zorder=5)
        ax.annotate(text, (q, v), xytext=offset, textcoords="offset points",
                    fontsize=9, color=TEXT, ha="left",
                    arrowprops=dict(arrowstyle="-", color=TEXT_MUTED, lw=0.8))

    # Bracket showing the gap between peaks.
    y = max(a_v, c_v) + 0.45
    ax.annotate("", xy=(c_q, y), xytext=(a_q, y),
                arrowprops=dict(arrowstyle="<->", color=TEXT_MUTED, lw=0.9))
    ax.text(a_q + (c_q - a_q) / 2, y + 0.06, f"{lag} quarters",
            ha="center", va="bottom", fontsize=9, color=TEXT_MUTED)

    ax.set_title("BNPL delinquencies peaked 7 quarters (21 months) before credit card delinquencies",
                 loc="left", fontsize=13, color=TEXT, pad=14)
    ax.set_xlabel("Quarter end", color=TEXT_MUTED, fontsize=9)
    ax.set_ylabel("30+ DPD rate (%)", color=TEXT_MUTED, fontsize=9)
    ax.set_ylim(0, y + 0.5)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}%"))
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=TEXT_MUTED, labelsize=9, length=0)
    ax.legend(loc="lower right", frameon=False, fontsize=9, labelcolor=TEXT)

    fig.text(0.01, 0.01,
             "Sources: Affirm 10-K/10-Q aging tables; FRED DRCCLACBS. "
             "Affirm has no 2020 Q3 filing (pre-IPO).",
             fontsize=7.5, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))

    out_path = OUT_DIR / "chart_lead_lag.png"
    fig.savefig(out_path, facecolor=SURFACE)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
