# Project Audible: BNPL vs Credit Card Credit Stress

FINTECH 590.05 Phase 4. Team: Samruddhi Shrawne and Abhinav Sharaff.
Defense date: October 28, 2026.

## Question
Is BNPL masking consumer credit stress that traditional credit card data misses?

## Repo structure
- `data/raw/` — unmodified pulls from FRED, EDGAR, CFPB
- `data/processed/` — cleaned CSVs ready for the dashboard
- `scripts/` — Python scripts that pull and clean the data
- `outputs/` — final charts, dashboard files
- `docs/` — position memo, technical memo
- `llm-log/` — LLM validation log

## Data sources
- FRED (Federal Reserve Economic Data)
- SEC EDGAR (Affirm 10-K/10-Q, Block 10-Q, PayPal 10-Q)
- CFPB BNPL market reports
