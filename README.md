# Project Audible: BNPL vs Credit Card Credit Stress

FINTECH 590.05 Phase 4. Duke M.Eng. Fintech, Fall 2026.
Team: Samruddhi Shrawne (data pipeline, analysis) and Abhinav Sharaff (dashboard, memos).
Defense: October 28, 2026.

## Question
Is BNPL masking consumer credit stress that traditional credit card data misses?

## Position
BNPL delinquencies lead credit card delinquencies by about 7 quarters. Watching only
credit card data gives a reader two years of false comfort before the same stress
shows up in traditional metrics.

## Headline evidence
- Affirm 30+ DPD peaked at 3.83% in Q3 2022.
- Credit card 30+ DPD (FRED DRCCLACBS, all commercial banks) peaked at 3.22% in Q2 2024.
- Cross-correlation across the full series peaks at a lag of 7-8 quarters (r = 0.76 in levels, 0.62 in quarter-over-quarter changes).
- Data covers one credit cycle (2020 Q2 to 2026 Q2, 24 quarters for Affirm).

## Repo structure
- `scripts/` — Python scripts for every data pull, parse, and chart
- `data/raw/` — Unmodified pulls from FRED and SEC EDGAR
- `data/processed/` — Clean quarterly CSVs used by the dashboard
- `outputs/` — Rendered chart
- `docs/` — Position memo, technical memo (TBA)
- `llm-log/` — LLM validation log (TBA)

## How to reproduce
1. `pip install pandas requests matplotlib`
2. `python scripts/pull_fred.py` (pulls FRED series, builds fred_quarterly.csv)
3. `python scripts/fetch_affirm_filings.py` (pulls Affirm filings from SEC EDGAR)
4. `python scripts/parse_affirm_delinquency.py` (parses delinquency tables, builds affirm_quarterly.csv)
5. `python scripts/chart_lead_lag.py` (renders the headline chart)
6. `python scripts/lead_lag.py` (prints the lag correlation table)

## Data sources
- FRED (Federal Reserve Economic Data): DRCCLACBS, CORCCACBS, PSAVERT, REVOLSL, TOTALSL
- SEC EDGAR: Affirm Holdings 10-K and 10-Q filings, 2021-2026
