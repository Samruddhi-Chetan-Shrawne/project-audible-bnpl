"""
parse_affirm_delinquency.py
Project Audible: BNPL vs Credit Card Credit Stress
FINTECH 590.05, Fall 2026

Reads every 10-K and 10-Q listed in data/raw/affirm/affirm_filings_index.csv
and extracts Affirm's aging analysis of loans by delinquency status. Each
filing shows two balance-sheet dates (the current period and a prior fiscal
year end); each becomes one row.

Affirm has used two layouts for this table:
  - By fiscal year of origination (September 2025 10-Q onward), one sub-table
    per date, loans held for investment only.
  - Totals only (earlier filings), one column per date. What it covers varies
    by filing: held for investment alone, or held for investment plus held for
    sale; the December 2020 10-Q uses unpaid principal balance rather than
    amortized cost.
The `basis` column records which one each row came from:
    hfi_by_origination  held for investment, by-origination table
    hfi                 held for investment, totals-only table
    hfi_hfs             held for investment + held for sale, amortized cost
    hfi_hfs_upb         held for investment + held for sale, unpaid principal
loans_held_for_investment_mil is the table total, so for hfi_hfs* rows it
includes loans held for sale. The basis follows each filing's own wording;
where filings with different wording report the same date, the totals match
exactly, so the series is comparable across bases in practice.

Metrics (from the Total column, in thousands):
    30+ DPD = (30-59 + 60-89 + 90-119) / Total
    90+ DPD = 90-119 / Total

Usage:
    python parse_affirm_delinquency.py

Output:
    data/processed/affirm_quarterly.csv (one row per quarter end, deduped to
    the most recently filed source)
"""

from pathlib import Path
from datetime import datetime
import html
import re
import pandas as pd

INDEX_PATH = Path("data/raw/affirm/affirm_filings_index.csv")
PROC_DIR = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

DATE_RE = r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}) ?, (\d{4})"
HEADER_RE = re.compile(r"Amortized Costs? Basis by Fiscal Year of Origination", re.I)
# Intro sentence of the totals-only table, up to the "(in thousands):" before the dates.
LEGACY_RE = re.compile(r"aging analysis of the ([^.]{0,200}?) by delinquency status \(in thousands\):", re.I)

# Row labels in table order. The dash between bucket bounds is an en dash in
# the HTML, so match any single non-word character there.
ROWS = [
    # Labeled "Non-delinquent loans" through the September 2025 10-Q.
    ("current",   r"Current\s*\W\s*3 calendar days past due|Non-delinquent loans"),
    ("d4_29",     r"4\s*\W\s*29 calendar days past due"),
    ("d30_59",    r"30\s*\W\s*59 calendar days past due"),
    ("d60_89",    r"60\s*\W\s*89 calendar days past due"),
    ("d90_119",   r"90\s*\W\s*119 calendar days past due"),
    ("total",     r"Total (?:amortized cost basis|unpaid principal balance)"),
]


def flatten(path: Path) -> str:
    """Strip tags and collapse whitespace so tables read as one line of text."""
    raw = path.read_bytes().decode("utf-8", errors="replace")
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text)


def row_values(segment: str) -> list[float]:
    """All cells in a row, left to right. A lone dash means zero."""
    segment = re.sub(r"\(\d\)", " ", segment)  # footnote markers like (1)
    cells = re.findall(r"\d[\d,]*|(?<!\w)[^\w\s$.,()](?!\w)", segment)
    if not cells:
        raise ValueError(f"no values in row: {segment!r}")
    return [float(c.replace(",", "")) if c[0].isdigit() else 0.0 for c in cells]


def to_iso(match: re.Match) -> str:
    month, day, year = match.groups()
    return datetime.strptime(f"{month} {day} {year}", "%B %d %Y").strftime("%Y-%m-%d")


def parse_rows(body: str) -> dict:
    """Split a table's text on the row labels; returns {row key: [cells]}."""
    end = re.search(ROWS[-1][1] + r"[^A-Za-z]*", body)
    if end is None:
        raise ValueError(f"no total row near: {body[:300]!r}")
    body = body[:end.end()]
    starts = [re.search(pat, body) for _, pat in ROWS]
    if any(s is None for s in starts):
        raise ValueError(f"missing row in table near: {body[:300]!r}")
    rows = {}
    for i, (key, _) in enumerate(ROWS):
        stop = starts[i + 1].start() if i + 1 < len(ROWS) else len(body)
        rows[key] = row_values(body[starts[i].end():stop])
    return rows


def check_total(vals: dict):
    buckets = sum(vals[k] for k, _ in ROWS[:-1])
    if abs(buckets - vals["total"]) > 2:  # allow rounding in thousands
        raise ValueError(f"buckets {buckets} != total {vals['total']}")


def extract_by_origination(text: str) -> list[dict]:
    """By-origination tables: one per date, Total is the last column."""
    out = []
    for m in HEADER_RE.finditer(text):
        body = text[m.end():m.end() + 3000]
        # Credit-quality (ITACs) and charge-off tables share the header; the
        # delinquency table is the one whose first row is the current bucket.
        first = re.search(ROWS[0][1], body)
        if not first or first.start() > 150:
            continue
        vals = {k: cells[-1] for k, cells in parse_rows(body).items()}
        check_total(vals)
        dates = list(re.finditer(DATE_RE, text[max(0, m.start() - 200):m.start()]))
        if not dates:
            raise ValueError(f"no date before table: {text[m.start() - 200:m.start()]!r}")
        vals["quarter_end"] = to_iso(dates[-1])
        vals["basis"] = "hfi_by_origination"
        out.append(vals)
    return out


def extract_totals_only(text: str) -> list[dict]:
    """Totals-only table: one column per date, dates listed in the header."""
    out = []
    for m in LEGACY_RE.finditer(text):
        described = m.group(1).lower()
        if "fiscal year of origination" in described:
            continue
        body = text[m.end():m.end() + 2000]
        first = re.search(ROWS[0][1], body)
        dates = [to_iso(d) for d in re.finditer(DATE_RE, body[:first.start()])]
        rows = parse_rows(body)
        if any(len(cells) != len(dates) for cells in rows.values()):
            raise ValueError(f"row widths {rows} don't match dates {dates}")

        if "held for sale" not in described:
            basis = "hfi"
        elif "unpaid principal" in described:
            basis = "hfi_hfs_upb"
        else:
            basis = "hfi_hfs"
        for i, date in enumerate(dates):
            vals = {k: cells[i] for k, cells in rows.items()}
            check_total(vals)
            vals["quarter_end"] = date
            vals["basis"] = basis
            out.append(vals)
    return out


def main():
    index = pd.read_csv(INDEX_PATH)
    index = index[index["form_type"].isin(["10-K", "10-Q"])]

    records = []
    for _, f in index.iterrows():
        path = Path(f["local_path"].replace("\\", "/"))
        text = flatten(path)
        tables = extract_by_origination(text) + extract_totals_only(text)
        print(f"  {f['form_type']:4} {f['report_date']} {f['accession']}: "
              f"{[(t['quarter_end'], t['basis']) for t in tables]}")
        for t in tables:
            records.append({
                "quarter_end": t["quarter_end"],
                "delinquency_30plus_pct": 100 * (t["d30_59"] + t["d60_89"] + t["d90_119"]) / t["total"],
                "delinquency_90plus_pct": 100 * t["d90_119"] / t["total"],
                "loans_held_for_investment_mil": t["total"] / 1000,
                "basis": t["basis"],
                "source_accession": f["accession"],
                "filing_date": f["filing_date"],
            })

    df = pd.DataFrame(records)
    df = (df.sort_values("filing_date")
            .drop_duplicates("quarter_end", keep="last")
            .sort_values("quarter_end")
            .drop(columns="filing_date")
            .reset_index(drop=True))
    df["delinquency_30plus_pct"] = df["delinquency_30plus_pct"].round(4)
    df["delinquency_90plus_pct"] = df["delinquency_90plus_pct"].round(4)
    df["loans_held_for_investment_mil"] = df["loans_held_for_investment_mil"].round(3)

    out_path = PROC_DIR / "affirm_quarterly.csv"
    df.to_csv(out_path, index=False)
    print(f"\nWrote {out_path}: {len(df)} quarters")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
