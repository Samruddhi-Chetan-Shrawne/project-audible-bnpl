"""
fetch_affirm_filings.py
Project Audible: BNPL vs Credit Card Credit Stress
FINTECH 590.05, Fall 2026

Pulls Affirm Holdings' (AFRM) filing history from SEC EDGAR and downloads
every 10-K, 10-Q, and 8-K from 2021 onward (post-IPO).

Produces:
    data/raw/affirm/affirm_filings_index.csv    (one row per filing: date, type, url, local path)
    data/raw/affirm/<accession>/<primary_doc>   (the actual filings)

Only external dependency: requests. SEC requires a descriptive User-Agent on
every request. Edit the EMAIL constant below so it is yours, not a placeholder.

Usage:
    python fetch_affirm_filings.py
"""

from pathlib import Path
import csv
import json
import time
import requests

CIK = "0001820953"  # Affirm Holdings, Inc.
TICKER = "AFRM"
EMAIL = "shrawnesamruddhi@gmail.com"  # SEC requires an identifying email
USER_AGENT = f"Project Audible FINTECH 590 - Samruddhi Shrawne {EMAIL}"
HEADERS = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"}

FILING_TYPES_WANTED = {"10-K", "10-Q", "8-K"}
START_YEAR = 2021  # Affirm IPO was January 2021

OUT_DIR = Path("data/raw/affirm")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def get_filings_json():
    """Hit SEC EDGAR submissions endpoint for the company."""
    url = f"https://data.sec.gov/submissions/CIK{CIK}.json"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def recent_filings(data):
    """Yield (date, type, accession, primary_doc) tuples from the submissions JSON."""
    recent = data["filings"]["recent"]
    for i, form in enumerate(recent["form"]):
        if form not in FILING_TYPES_WANTED:
            continue
        date = recent["filingDate"][i]
        if int(date[:4]) < START_YEAR:
            continue
        yield {
            "date": date,
            "type": form,
            "accession": recent["accessionNumber"][i],
            "primary_doc": recent["primaryDocument"][i],
            "report_date": recent["reportDate"][i],
        }


def download(filing):
    """Download the primary document for one filing."""
    acc = filing["accession"].replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc}/{filing['primary_doc']}"
    local_dir = OUT_DIR / filing["accession"]
    local_dir.mkdir(exist_ok=True)
    local_path = local_dir / filing["primary_doc"]
    if local_path.exists():
        return url, local_path, "cached"
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    local_path.write_bytes(r.content)
    time.sleep(0.15)  # polite: SEC asks for <= 10 requests per second
    return url, local_path, "downloaded"


def main():
    print(f"Fetching EDGAR submissions for {TICKER} (CIK {CIK})...")
    data = get_filings_json()
    filings = list(recent_filings(data))
    print(f"Found {len(filings)} filings of type {FILING_TYPES_WANTED} since {START_YEAR}")

    index = []
    for i, f in enumerate(filings, 1):
        print(f"  [{i}/{len(filings)}] {f['date']} {f['type']} ({f['primary_doc']})...", end=" ")
        try:
            url, local_path, status = download(f)
            print(status)
            index.append({
                "filing_date": f["date"],
                "report_date": f["report_date"],
                "form_type": f["type"],
                "accession": f["accession"],
                "primary_doc": f["primary_doc"],
                "edgar_url": url,
                "local_path": str(local_path),
            })
        except Exception as e:
            print(f"FAILED: {e}")

    idx_path = OUT_DIR / "affirm_filings_index.csv"
    with idx_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(index[0].keys()))
        w.writeheader()
        w.writerows(index)
    print(f"\nWrote {idx_path}: {len(index)} rows")
    print("\nFilings to use for delinquency data: all 10-Q and 10-K entries.")
    print("Open each, locate the 'Delinquency' or 'Credit Quality' table, type")
    print("the 30+ DPD rate into affirm_delinquency_raw.csv.")


if __name__ == "__main__":
    main()
