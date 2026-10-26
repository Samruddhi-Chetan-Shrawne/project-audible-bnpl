"""
pull_fred.py
Project Audible: BNPL vs Credit Card Credit Stress
FINTECH 590.05, Fall 2026

Pulls five FRED series into data/raw/ as CSVs, then builds one quarterly
aggregate at data/processed/fred_quarterly.csv for the dashboard.

Series:
  DRCCLACBS : Delinquency Rate on Credit Card Loans, All Commercial Banks (quarterly, %)
  CORCCACBS : Charge-Off Rate on Credit Card Loans, All Commercial Banks (quarterly, %)
  PSAVERT   : Personal Saving Rate (monthly, %)
  REVOLSL   : Revolving Consumer Credit Owned and Securitized (monthly, $B)
  TOTALSL   : Total Consumer Credit Owned and Securitized (monthly, $B)

No API key needed - uses FRED's public CSV download URL.

Usage:
    python pull_fred.py

Outputs:
    data/raw/DRCCLACBS.csv            (raw FRED pull)
    data/raw/CORCCACBS.csv
    data/raw/PSAVERT.csv
    data/raw/REVOLSL.csv
    data/raw/TOTALSL.csv
    data/processed/fred_quarterly.csv (one row per quarter, all series joined)
"""

from pathlib import Path
import urllib.request
import pandas as pd

SERIES = ["DRCCLACBS", "CORCCACBS", "PSAVERT", "REVOLSL", "TOTALSL"]
START = "2019-01-01"
END   = "2026-06-30"

RAW_DIR  = Path("data/raw")
PROC_DIR = Path("data/processed")
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


def pull(series_id: str) -> pd.DataFrame:
    """Download one FRED series as a dataframe, write a raw copy to data/raw/."""
    url = (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}&cosd={START}&coed={END}"
    )
    out = RAW_DIR / f"{series_id}.csv"
    urllib.request.urlretrieve(url, out)
    df = pd.read_csv(out)
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    print(f"  {series_id}: {len(df)} rows, {df['date'].min().date()} to {df['date'].max().date()}")
    return df


def to_quarterly(df: pd.DataFrame, series_id: str, how: str = "mean") -> pd.DataFrame:
    """Collapse to quarter-end. Credit card series are already quarterly."""
    df = df.set_index("date")
    if how == "mean":
        q = df[series_id].resample("QE").mean()
    else:
        q = df[series_id].resample("QE").last()
    return q.to_frame().reset_index().rename(columns={"date": "quarter"})


def main():
    print("Pulling FRED series...")
    frames = {sid: pull(sid) for sid in SERIES}

    print("\nAggregating to quarterly...")
    # Credit card series are already reported quarterly; monthly series we average.
    quarterly = {
        "DRCCLACBS": to_quarterly(frames["DRCCLACBS"], "DRCCLACBS", "last"),
        "CORCCACBS": to_quarterly(frames["CORCCACBS"], "CORCCACBS", "last"),
        "PSAVERT":   to_quarterly(frames["PSAVERT"],   "PSAVERT",   "mean"),
        "REVOLSL":   to_quarterly(frames["REVOLSL"],   "REVOLSL",   "last"),
        "TOTALSL":   to_quarterly(frames["TOTALSL"],   "TOTALSL",   "last"),
    }

    out = quarterly["DRCCLACBS"]
    for sid in ["CORCCACBS", "PSAVERT", "REVOLSL", "TOTALSL"]:
        out = out.merge(quarterly[sid], on="quarter", how="outer")

    out = out.sort_values("quarter").reset_index(drop=True)
    out["quarter"] = out["quarter"].dt.strftime("%Y-%m-%d")

    out = out.rename(columns={
        "DRCCLACBS": "cc_30plus_dpd_rate_pct",
        "CORCCACBS": "cc_nco_rate_pct",
        "PSAVERT":   "personal_savings_rate_pct",
        "REVOLSL":   "revolving_consumer_credit_bil",
        "TOTALSL":   "total_consumer_credit_bil",
    })

    out_path = PROC_DIR / "fred_quarterly.csv"
    out.to_csv(out_path, index=False)
    print(f"\nWrote {out_path}: {len(out)} quarters, {len(out.columns)-1} series")
    print(out.tail(8).to_string(index=False))


if __name__ == "__main__":
    main()
