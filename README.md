# Project Audible: BNPL vs Credit Card Credit Stress
**Live dashboard:** https://samruddhi-chetan-shrawne.github.io/project-audible-bnpl/dashboard/

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
- `dashboard/` — Interactive dashboard (executive, analyst and regulator pages with drill-through)
- `outputs/` — Rendered chart
- `docs/` — Position memo (`position_memo.md`) and technical memo (`technical_memo.md`)
- `llm-log/` — LLM validation log (`validation_log.md`)

## How to reproduce
1. Set up the environment (Python 3.11+):
   ```
   python3 -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. `python scripts/pull_fred.py` (pulls FRED series, builds fred_quarterly.csv)
3. `python scripts/fetch_affirm_filings.py` (pulls Affirm filings from SEC EDGAR)
4. `python scripts/parse_affirm_delinquency.py` (parses delinquency tables, builds affirm_quarterly.csv)
5. `python scripts/chart_lead_lag.py` (renders the headline chart)
6. `python scripts/lead_lag.py` (prints the lag correlation table)
7. `python scripts/build_dashboard_data.py` (builds dashboard/data.js, the one data model all dashboard pages read)
8. Open `dashboard/index.html` in a browser. It runs offline; Plotly is saved in `dashboard/vendor/`.

## Dashboard
One data model, three pages (FINTECH 590 Lecture 3):
- **Executive**: conclusion card, recommendation, one supporting chart. Click the card or any point to drill through.
- **Analyst**: slicers for window, measure, levels vs. changes, and lag. Every measure recalculates live; includes the position ledger, measure definitions and row-level data.
- **Regulator**: neutral descriptive titles, data vintage, a source register linking every quarter to its SEC filing, and a source chain for every headline figure.

Correlation intervals are sized to the effective number of independent quarter pairs (Pyper & Peterman 1998), since both series are strongly autocorrelated. The position ledger also reports a phase-randomized null test across all 11 lags, prewhitened and year-over-year versions of the lag test, and a drop-one-quarter check.

**Export PDF** (header button, or open `#print`) lays out all three pages on landscape letter sheets. Presenter keys: `1` `2` `3` switch pages, `←` `→` step through a drill-through, `Esc` goes back.

## Data sources
- FRED (Federal Reserve Economic Data): DRCCLACBS, CORCCACBS, PSAVERT, REVOLSL, TOTALSL
- SEC EDGAR: Affirm Holdings 10-K and 10-Q filings, 2021-2026
