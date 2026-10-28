# LLM Validation Log

**Project Audible**
**FINTECH 590.05, Fall 2026**
**Team:** Samruddhi Shrawne, Abhinav Sharaff
**Date:** October 28, 2026

This log records every use of a large language model on this project, the prompts and outputs that mattered, how each output was validated, and which decisions and numbers remain under human ownership.

## Inventory of LLM uses

| # | Tool | Model and version | Date | Task |
|---|---|---|---|---|
| 1 | Claude.ai (web) | Opus 4.7 | Oct 25-26, 2026 | Phase 4 project framing: translating Marvin's Phase 1 critique into actionable fixes, picking data sources, choosing the comparable loss measure, drafting memo structure |
| 2 | Claude Code CLI | Opus 5.5 (Claude Pro) | Oct 26, 2026 | Parsing Affirm 10-K and 10-Q HTML filings to extract delinquency tables; writing the chart script; running the cross-correlation analysis |
| 3 | Claude.ai (web) | Opus 4.7 | Oct 26, 2026 | Writing first drafts of the position memo and this validation log |
| 4 | Claude Code | Opus 5.5 | Oct 27, 2026 | Building the three-audience dashboard, `build_dashboard_data.py`, and the robustness checks in the position ledger |
| 5 | Claude Code (VS Code extension) | Opus 5.5 | Oct 28, 2026 | Moving the memos into the repo and updating them to reflect the dashboard and robustness results |

No other LLMs or AI tools were used.

## Key prompts and outputs

### Use 1: Project framing (Claude.ai)

**Context.** After receiving Marvin's Phase 1 feedback (score 13.5 out of 20, with four criticisms: inconsistent charge-off definitions, Klarna's SEC filing gap, Affirm's bureau furnishing, and missing "now what"), we needed to decide which fixes to make.

**Representative prompt.** "Marvin's critique on the Phase 1 pitch includes: charge-offs not consistently defined, Klarna doesn't file US 10-K/Q, Affirm started reporting to credit bureaus, framing missing 'now what'. Help me decide what to swap and what to defend."

**Output summary.** The model proposed four fixes: build our own 30+ DPD measure as the comparable loss metric, drop Klarna and swap in Block (Afterpay) and PayPal (Pay in 4), narrow the invisible-to-bureaus framing, and name a specific audience for the recommendation (CFPB or bank risk teams).

**Validation.** Each proposed fix was checked against the Phase 1 critique and against what Affirm's actual 10-Q disclosures contain. The 30+ DPD proposal was validated by locating the aging analysis table in Affirm's March 31, 2026 10-Q and confirming the bucket structure matched. The Block/PayPal swap was ultimately not executed because their BNPL disclosures sit inside segment aggregates. See the technical memo "What was tried and rejected" section.

**Human-owned decisions.**
- Decision to drop Klarna: human.
- Decision to skip Block and PayPal: human, after reviewing the model's analysis.
- Final audience choice ("Supervisory Policy Committee and bank CROs"): human.
- Decision to use peak comparison plus cross-correlation rather than peak-only: human, prompted by the model raising the one-point-test risk.

### Use 2: Data parsing and analysis (Claude Code)

**Context.** 23 Affirm 10-K and 10-Q filings needed to be parsed to extract delinquency buckets. Hand-typing was estimated at 30-45 minutes with meaningful error risk.

**Representative prompts.**
- "For each 10-K and 10-Q in the index, parse the HTML file and find the aging analysis table. Compute 30+ DPD = (30-59 + 60-89 + 90-119) / Total. Write to data/processed/affirm_quarterly.csv."
- "Add the older Affirm filings (through 2020) using the simpler aging table they report, with a basis column flagging which balance base each row uses."
- "Build a chart with Affirm 30+ DPD and FRED credit card 30+ DPD on one axis from 2020 Q2 to 2026 Q2. Annotate each peak."
- "Compute Pearson correlation between Affirm 30+ DPD and credit card 30+ DPD at lags 0 through 10 quarters."

**Validation.** For every parsed table, Claude Code built in a bucket-sum check (buckets must equal reported total within 2 thousand dollar rounding). Human checks on top:
- March 31, 2026 was manually verified against the raw 10-Q HTML. The sum of the 30-59, 60-89, and 90-119 buckets ($93,578K + $78,167K + $64,553K = $236,298K) divided by Total ($8,483,593K) gives 2.785%, matching the pipeline output exactly.
- June 30, 2025 was manually verified the same way: $171,309K / $6,957,582K = 2.462%, matching the pipeline output exactly.
- The peak values from the chart (Affirm 3.83% Q3 2022, credit cards 3.22% Q2 2024) were cross-checked against the raw CSVs.
- The correlation table was sanity-checked for monotonic rise and fall rather than random noise, consistent with a real lead-lag relationship.

**Issues found and corrected.**
- Initial parser missed older filings because Affirm renamed "Non-delinquent loans" to "Current to 3 calendar days past due" in September 2025. Human review of parser output caught the gap. Claude Code was instructed to extend the regex to accept both labels.
- The chart initially drew a straight line through a missing 2020 Q3 data point (Affirm had no filing that quarter, pre-IPO). Human review of the rendered PNG caught the artifact. Claude Code was instructed to break the line at missing quarters.
- Initial correlation was computed on levels only. Human requested the quarter-over-quarter changes variant as a drift control. Claude Code added it.

**Human-owned decisions.**
- Choice of 30+ DPD as the comparable loss measure: human, from Use 1.
- Choice to run the lag correlation up to 10 quarters: human.
- Choice to include the changes-based correlation as a second test: human.
- Decision to accept the 7 to 8 quarter lead as the headline finding: human.

### Use 3: Memo drafting (Claude.ai)

**Context.** First drafts of the position memo and this validation log were produced in the Claude.ai chat.

**Representative prompt.** "Draft the position memo, 2 pages max, Backwards First structure. Numbers must tie to our actual pulls. No em dashes, no 'this rather than that' phrasing."

**Output summary.** Full draft of the position memo and this validation log, ready for human review and finalization.

**Validation.** Every number cited in the memo was cross-checked against the processed CSVs and the chart. Specifically:
- "Affirm 30+ DPD peaked in Q3 2022 at 3.83%" verified against `affirm_quarterly.csv`.
- "Credit card 30+ DPD peaked in Q2 2024 at 3.22%" verified against `fred_quarterly.csv`.
- "7 quarters" verified by counting the quarters between September 30, 2022 and June 30, 2024.
- "r = 0.76 at lag 8, r = 0.62 at lag 7 on changes" verified against `lead_lag.py` output.

**Human-owned decisions and finalization.**
- Final memo wording, tone, and length are the responsibility of Abhinav Sharaff for submission.
- All numerical claims in the final submission will be reconciled against the committed CSVs one more time before submission.
- The team is responsible for every claim in the final submission, regardless of whether the first-draft text came from an LLM.

### Use 4: Dashboard and robustness checks (Claude Code)

**Context.** The dashboard needed to serve three audiences (executive, analyst, regulator) from one data model, following the Lecture 3 structure, and the single-cycle limitation needed to be tested more rigorously than the two correlation tests in Use 2.

**Task given to the model.** Build `scripts/build_dashboard_data.py` to produce one data model (`dashboard/data.js`) from the committed CSVs, and a static, offline dashboard with executive, analyst and regulator pages and drill-through. Add robustness checks that try to break the headline claim: autocorrelation-adjusted intervals, a phase-randomized null test across all lags, prewhitened and year-over-year versions of the lag test, and a drop-one-quarter check.

**Validation.**
- `build_dashboard_data.py` imports the lag functions and analysis window from `lead_lag.py` rather than reimplementing them, so the dashboard and the printed lag table cannot drift apart. The dashboard's levels and changes results (8 quarters r = 0.76, 7 quarters r = 0.62) match `lead_lag.py` output exactly.
- `data.js` is stamped with its build time and the pipeline commit so a reviewer can tie any dashboard number to a specific version of the code.
- Every row on the regulator page's source register links to the SEC filing it came from.
- The checks were written as falsification tests, each with a stated condition that would break the claim. Four of them came back Narrow instead of Hold (null test at 5.4%, wide adjusted interval, trough timing, denominator growth). We kept those results and reported them in the position memo instead of tuning the tests until they passed.

**Human-owned decisions.**
- The three audiences and what each page should answer: human.
- Which robustness checks to run and the threshold that counts as breaking each claim: human, with the model proposing candidates.
- Reporting Narrow verdicts in the memo as limitations: human.

### Use 5: Memo finalization (Claude Code)

**Context.** The memo drafts from Use 3 predated the dashboard and were kept in a local folder that was not committed.

**Task given to the model.** Move the memos into `docs/` and `llm-log/`, and update them to reflect the dashboard, the robustness results, and the full pipeline.

**Validation.** The model reran `lead_lag.py` and read the generated position ledger before editing, and every number it added traces to those outputs. It also fixed an inconsistency in the first draft, which said the trigger gives card teams "six to nine months", while the 7-quarter lead and the trigger test both imply more than a year.

## Clear statement of human ownership

The following items are human-made or human-verified and not LLM-generated:

- Choice of research question and position (BNPL as a leading indicator).
- Choice of comparable loss measure (30+ DPD on amortized cost).
- Decision to drop Klarna and skip Block and PayPal.
- Final audience for the "now what" recommendation.
- Every numerical claim in the memos, each manually recomputed from the CSVs or independently derived from the raw filings.
- The chart's title language and axis choices.
- Final memo wording, length, and submission.

The following items are LLM-generated and human-reviewed:

- First drafts of memo prose.
- Python code for data parsing, chart generation, correlation analysis, robustness checks, and the dashboard.
- Initial structure and section headings in all three memos.

LLM-generated code was executed, outputs were cross-checked against raw filings for sample quarters, and bucket-sum assertions in the parser caught any arithmetic errors before they reached the dashboard or memos.
