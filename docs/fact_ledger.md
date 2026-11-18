# Project Audible — Fact Ledger

**FINTECH 590.05 · Duke M.Eng. FinTech · Fall 2026**
**Team:** Samruddhi Shrawne, Abhinav Sharaff
**Analysis window:** 2026-06-30 (data pulled 2026-10-26)

A traceable reference for every figure cited in the Project Audible dashboard and memos. Each row names the claim, its value, the source it comes from (a FRED series, an SEC filing, or a script in this repository), and the as-of date. Any figure quoted in the project should match its row here. The "Cited in" column records which of the dashboard's three audience views (Executive, Risk, Compliance) uses the number.

## The project in one paragraph

Project Audible tests whether Buy Now Pay Later delinquency data gives an earlier warning of consumer credit stress than bank credit card data alone. Using one BNPL lender (Affirm, the only large pure-play BNPL firm filing with the SEC) and the Federal Reserve's bank card delinquency series, we find that both the inverted personal saving rate and Affirm's 30-day delinquency rate rose roughly seven quarters before bank card delinquencies peaked during the 2020–2024 cycle. The saving rate gives the first warning; Affirm's rate confirms that household stress has reached consumer loan books. We recommend watching both series together, with a +0.50 percentage point year-over-year rise in Affirm's rate as the signal to re-examine a card lending portfolio. The finding rests on a single credit cycle and is presented as a pattern, not a forecast.

## The ledger

| ID   | Claim | Value | Source | As-of | Cited in |
| ---- | ----- | ----- | ------ | ----- | -------- |
| F-01 | Affirm Holdings 30-day delinquency rate, peak | 3.83% | 10-Q filed 2022-11-08 (SEC accession 0001820953-22-000039); aging buckets 30–59 + 60–89 + 90–119 days divided by total amortized cost | 2022-09-30 | Executive · Risk · Compliance |
| F-02 | Bank credit card 30-day delinquency rate, peak | 3.22% | Federal Reserve series DRCCLACBS (all commercial banks, seasonally adjusted) via FRED | 2024-06-30 | Executive · Risk · Compliance |
| F-03 | Quarters between the two peaks | 7 quarters (21 months) | F-02 quarter minus F-01 quarter | — | Executive · Risk · Compliance |
| F-04 | Correlation between Affirm and card delinquency rates, levels | r = 0.76 at an 8-quarter lead (r = 0.74 at a 7-quarter lead), 16 overlapping quarter pairs (about 7 independent pairs after adjusting for serial correlation) | `scripts/lead_lag.py`, Pearson correlation on raw rates | pulled 2026-10-26 | Risk · Compliance |
| F-05 | Same correlation on quarter-over-quarter changes | r = 0.62 at a 7-quarter lead, 15 pairs | `scripts/lead_lag.py`, first-differenced rates. Strips out shared drift between the two series | pulled 2026-10-26 | Executive · Risk · Compliance |
| F-06 | 95% range on the peak correlation, adjusted for serial correlation | +0.03 to +0.96 | Pyper & Peterman (1998) adjustment to the effective sample size | pulled 2026-10-26 | Risk · Compliance |
| F-07 | Random-series null test | 5.4% of 10,000 synthetic series with the same autocorrelation matched or beat our lead across the 11 lags tested | `scripts/build_dashboard_data.py`, phase-randomized surrogates | pulled 2026-10-26 | Risk · Compliance |
| F-08 | Proposed monitoring rule | Review the card lending portfolio when Affirm's 30+ day delinquency rate rises by 0.50 percentage points or more compared to the same quarter a year earlier | `scripts/build_dashboard_data.py` | — | Executive · Risk · Compliance |
| F-09 | History of the F-08 rule across the sample | Fired at Affirm's Q4 2021 10-Q (filed 2022-02-14), 10 quarters before the card peak. One false alarm at the Q2 2024 10-Q, with no card rise in the eight quarters after | Derived from F-08 and the Affirm series | pulled 2026-10-26 | Executive · Risk · Compliance |
| F-10 | F-08 rule status at the end of the analysis window | Not triggered. Affirm's rate was +0.05 percentage points higher than a year earlier | Dashboard Executive page | 2026-06-30 | Executive · Risk · Compliance |
| F-11 | Analysis coverage | 24 observed Affirm quarters from Q2 2020 to Q2 2026. Q3 2020 is absent because Affirm was pre-IPO and did not file with the SEC that quarter | `data/processed/affirm_quarterly.csv` | pulled 2026-10-26 | Executive · Risk · Compliance |
| F-12 | Robustness ledger summary | 14 falsification tests on the finding: 8 hold the claim; 6 narrow it (see dashboard Risk page for the full list) | Dashboard Risk page position ledger | pulled 2026-10-26 | Risk · Compliance |
| F-13 | Data vintage | SEC EDGAR and FRED pulled 2026-10-26 (frozen). Dashboard `data.js` last rebuilt 2026-11-17 22:19 UTC at commit 07d7b0e | Dashboard Compliance page | 2026-11-17 | Risk · Compliance |
| F-14 | Affirm Q3 2026 10-Q (ingested after the analysis window was frozen) | 2.95%, a 0.07 percentage point rise year-over-year | 10-Q filed 2026-11-05 (SEC accession 0001628280-26-071153) | 2026-09-30 | Executive · Risk · Compliance |
| F-15 | Correlation between inverted personal saving rate and card delinquency, levels | r = 0.92 at a 7-quarter lead, 18 pairs (also r = 0.92 at 8 quarters) | FRED series PSAVERT with the sign flipped (so a falling saving rate reads as rising stress); `scripts/lead_lag.py` extended | pulled 2026-10-26 | Executive · Risk · Compliance |
| F-16 | Same correlation on quarter-over-quarter changes | r = 0.47 at an 8-quarter lead, 16 pairs. Note: Affirm beats the saving rate on this test (F-05, r = 0.62) | FRED PSAVERT, first-differenced | pulled 2026-10-26 | Risk · Compliance |
| F-17 | Partial correlation of Affirm with cards, controlling for the saving rate | r = 0.66 (raw r = 0.84) at an 8-quarter lead, from 2021 onward, 14 pairs. Partial correlation isolates the piece of the Affirm-card relationship not explained by the saving rate | Residual-on-residual Pearson after regressing each series on the saving rate | pulled 2026-10-26 | Risk |
| F-18 | Personal saving rate around the Q4 2021 F-08 trigger | 7.0% at 2021-12-31 (near the 2019 average of 7.3%), falling to 3.9% at 2022-03-31 | FRED PSAVERT, quarter-end values | 2021-12-31 and 2022-03-31 | Executive · Risk |
| F-19 | Personal saving rate at the end of the analysis window | 4.4% (compared with a 2019 average of 7.3%) | FRED PSAVERT, quarter-end | 2026-06-30 | Executive · Risk · Compliance |

## Terms used in the ledger

- **30-day delinquency rate (30+ DPD).** Share of the total loan balance that is at least 30 days past due at the end of the quarter. For Affirm, this is computed from the aging-analysis table in each 10-K or 10-Q: the sum of the 30–59, 60–89, and 90–119 day buckets divided by the total amortized cost of loans held for investment. For bank credit cards, it is the Federal Reserve's DRCCLACBS series, which the Fed compiles quarterly from Call Reports submitted by all US commercial banks.
- **Percentage point (pp).** The arithmetic difference between two percentages. A move from 2.5% to 3.0% is +0.5 percentage points, not +0.5 percent.
- **Year-over-year (YoY).** Change versus the same quarter one year earlier. The +0.50 pp YoY rule compares a quarter's rate to its own value four quarters ago, not to the previous quarter.
- **Lead and lag.** We shift one series in time by a fixed number of quarters and measure the relationship with the other. "A 7-quarter lead" means Affirm's rate in quarter t is compared with cards' rate in quarter t + 7. The relationship between the two series is strongest at a 7- to 8-quarter shift.
- **Levels vs changes.** The levels test uses the raw rates. The changes test uses the quarter-over-quarter difference. The changes test is harder to pass: it removes any shared trend between the two series, so it isolates whether their movements actually line up in time.
- **Pearson correlation (r).** A standard −1 to +1 measure of how closely two variables move together. r = 1 is a perfect positive relationship, r = 0 is none, r = −1 is a perfect negative relationship. Significance depends on the effective sample size, which for autocorrelated series like these is smaller than the raw pair count (see F-06).
- **Effective sample size.** The number of statistically independent observations after accounting for serial correlation in both series. The two tests we use (Pyper-Peterman adjustment and a phase-randomized null) both bring this down from about 16 raw pairs to about 7 effective pairs.
- **10-K and 10-Q.** Public annual and quarterly reports that US-listed companies file with the Securities and Exchange Commission. Accessible through SEC EDGAR. Each cited figure in the ledger links back to the specific filing by accession number.
- **FRED.** Federal Reserve Economic Data, published by the St. Louis Fed. A free public archive of US macroeconomic time series. Series used here are DRCCLACBS (card delinquency) and PSAVERT (personal saving rate).

## Data notes

- **Analysis window.** Q2 2020 to Q2 2026 (24 observed Affirm quarters). The window ends in June 2026 because that is the most recent quarter with data from both Affirm and the Federal Reserve's card series available on 2026-10-26, the date of the pull used by the dashboard.
- **Missing quarter.** There is no Affirm figure for Q3 2020 (F-11). Affirm went public in January 2021; before then it did not file with the SEC. The first SEC filing with the required aging table was the 10-Q for the quarter ended December 31, 2020 (filed February 2021), which reported Q2 2020 and Q4 2020 but not Q3 2020.
- **Saving rate sign convention.** FRED's PSAVERT rises when households save more. For the lead-lag tests, we flip the sign so that a falling saving rate reads as rising household stress, directionally comparable to a rising delinquency rate (F-15, F-16).
- **Revisions.** Bank card and saving rate series from FRED are periodically revised. The values in this ledger match the pull made on 2026-10-26 (F-13). A reproduction run on 2026-11-17 found the three analysis series (DRCCLACBS, CORCCACBS, PSAVERT) unchanged.

## Reproducibility

Every figure in this ledger is produced by code in this repository. One command rebuilds the full analysis from a clean environment:

    ./run_demo.sh

See `README.md` for prerequisites, `docs/technical_memo.md` for the pipeline design, and `docs/cold_start_log.md` for a documented reproduction on a different machine.
