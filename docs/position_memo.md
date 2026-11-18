# Position Memo: BNPL as a Loan-Level Confirmation of Household Stress

**To:** Supervisory Policy Committee and bank Chief Risk Officers
**From:** Samruddhi Shrawne and Abhinav Sharaff
**Date:** November 18, 2026
**Re:** Including BNPL delinquency data alongside the personal saving rate in consumer-credit early-warning dashboards

## Recommendation

The saving rate gives the first warning; Affirm confirms stress has reached loan books. Add both to consumer-credit early-warning dashboards. Treat a +0.50 percentage-point year-over-year rise in Affirm's 30+ day delinquency rate as the trigger for a card book review.

Affirm's 30+ DPD peaked **7 quarters** before the Federal Reserve's bank credit card series did (Affirm Q3 2022, cards Q2 2024). The inverted personal saving rate's sharpest move preceded Affirm's peak by another three quarters, dropping from 7.0% at Q4 2021 to 3.9% at Q1 2022. Across the whole series, cross-correlation peaks at a **7 to 8 quarter lead** on both measures — the two tests agree. The card-only dashboard missed the warning both the saving rate and Affirm already gave.

## Evidence

**Peak comparison.** Affirm Holdings is the largest pure-play US BNPL lender filing a 10-K and 10-Q with the SEC. Its 30+ day delinquency rate on loans held for investment — the sum of the 30–59, 60–89, and 90–119 day aging buckets divided by total amortized cost — rose from 1.00% at Q4 2020 to 3.83% at Q3 2022 before falling back to 1.97% by Q2 2023. The Fed's DRCCLACBS series, which tracks 30+ day delinquency on card loans at all commercial banks, rose from 1.53% at Q3 2021 to 3.22% at Q2 2024. The gap between the two peaks is 7 quarters (21 months). The inverted personal saving rate dropped from roughly its pre-pandemic level (7.0% at Q4 2021, versus a 2019 average of 7.3%) to 3.9% at Q1 2022, 9 quarters before the card peak, and bottomed at 2.6% in Q2 2022.

**Cross-correlation across the whole series.** Pearson correlation between Affirm 30+ DPD and card 30+ DPD across 24 observed quarters (Q3 2020 has no Affirm filing) rises from −0.09 at zero lag to +0.76 at an 8-quarter lead on 16 overlapping pairs, where the levels correlation peaks. The same correlation on quarter-over-quarter changes, which strips out shared drift, peaks at +0.62 at a 7-quarter lead on 15 pairs. The inverted saving rate against cards gives +0.92 at a 7-quarter lead on 18 pairs in levels and +0.47 at an 8-quarter lead on 16 pairs in changes. Every variant — Affirm, saving rate, levels, changes, prewhitened (+0.58 at 7-quarter), and year-over-year (+0.75 at 7-quarter) — lands at a 7 or 8 quarter lead. None lands outside that window.

**Partial correlation.** The saving rate carries the higher raw correlation, but Affirm retains independent information. Controlling for the saving rate, Affirm's partial correlation with cards at an 8-quarter lead is +0.66 (raw +0.83) on 14 pairs from 2021 onward. The partial collapses at lags 5 to 7, so this is consistent with the story rather than proof: the two signals are correlated — they both measure household stress — but they fail differently. The saving rate is a macro aggregate of household cash flow; Affirm measures actual missed loan payments. In the changes test, which is methodologically stronger, Affirm beats the saving rate (0.62 vs 0.47).

**Economic rationale.** BNPL loans have shorter tenors than credit cards. Pay-in-four products settle in six weeks, installment loans in six to twelve months. A stressed BNPL borrower reaches a delinquency bucket in weeks. A stressed card borrower can ride a revolving line for months. The BNPL lead is mechanical, not predictive magic. The saving rate lead is prior to both: it measures the cash squeeze that precedes any missed loan payment.

**Trigger rationale.** Across our 20 observable Affirm YoY changes, the four 2021-2022 cluster readings sit between +1.23 and +2.46 percentage points, and the next-highest reading is +0.55. Any threshold between +0.56 and +1.22 gives the same signal in this sample. We chose +0.50 because it sits in the natural gap, is a round number, and accepts one in-sample false alarm (Q2 2024) rather than risk missing a smaller true signal in a future cycle. A +0.75 threshold would give zero false alarms in this cycle at the cost of some sensitivity in the next one; the recommendation is unchanged if a reviewing committee prefers it.

## Counterarguments and limitations

**The saving rate alone is enough.** It publishes monthly from BEA with about a four-week lag, faster than Affirm's 40-day quarterly filing cycle, and carries a higher levels correlation. We are not proposing dropping it. We are proposing pairing it with Affirm so that false alarms in one are cheap to dismiss when the other does not confirm.

**Different borrower pools.** BNPL customers skew younger, thinner-file, and lower-income than card holders. The position does not require identical populations, only that stress in BNPL borrowers moves ahead of stress in bureau-reported borrowers. That holds across every variant of the test.

**Affirm reports to Experian since April 2022; FICO shipped a BNPL score in October 2025.** Bureau integration narrows the lead as BNPL feeds bureaus with full history. Affirm is still the fastest public read on borrower-level BNPL stress and does not require a vendor subscription. The marginal value shrinks over time; the directional claim does not.

**Affirm's book has shifted to longer tenor and more prime borrowers through Chase and Shopify.** The denominator growing 3.6x is why the rate fell after 2022 while late balances rose from $102M to $238M. The +0.50 YoY trigger normalizes to the current book. A precise 7-quarter forecast on the new mix would need a second cycle to re-fit.

**One credit cycle.** The analysis covers Q2 2020 to Q2 2026. Cross-correlation on 24 observed quarters carries about 7 independent pairs after autocorrelation adjustment, so the 95% range on the peak correlation is wide (+0.03 to +0.96). Random look-alike series with the same autocorrelation match our lead 5.4% of the time across 11 tested lags, just above the conventional 5% bar. The robustness ledger shows 8 of 14 checks hold and 6 narrow the claim. The direction and timing are the durable finding; the 7-quarter number is the best estimate from the cycle we have, and a slower cycle would likely shorten it.

**Why the position still holds.** The asymmetric cost of ignoring either signal is high. A 7-quarter lead that is directionally correct is more valuable than one that is precisely measured. A false alarm costs one analyst review. Missing a real signal costs 21 months of lead time. Adding both series to an existing dashboard is low cost; ignoring them means waiting for cards to confirm what the saving rate and Affirm already said.

## Now what

Three concrete steps for supervisory bodies and bank risk teams:

1. **Watch the saving rate as the primary macro signal.** Monthly BEA release, four-week lag. Already on most macro dashboards — formalize it as a consumer-credit leading indicator rather than a general macro one.
2. **Watch Affirm's 30+ DPD as loan-level confirmation.** Public in Affirm's 10-K and 10-Q filings, 40-day lag. A +0.50 percentage-point year-over-year rise is the signal to re-examine the card lending portfolio. In this sample the trigger fired at the Q4 2021 10-Q, 10 quarters before the card peak. At Q2 2026 the rate is +0.05 points year over year — watch, not review.
3. **Request comparable data from Afterpay (Block), Klarna, and PayPal.** Block and PayPal file 10-Ks and 10-Qs but disclose BNPL inside segment aggregates. Supervisory data calls could standardize aging-bucket disclosures across the category. This separates a product effect from a lender effect and gives a second cycle of observations for threshold calibration.

The dashboard, reproducible pipeline, fact ledger, and audit trail are at `github.com/Samruddhi-Chetan-Shrawne/project-audible-bnpl`. The analysis window is frozen at Q2 2026 with data pulled 2026-10-26; the dashboard's `data.js` was last rebuilt 2026-11-17 at commit `07d7b0e`. One command — `./run_demo.sh` — rebuilds the whole analysis from a clean environment; see `docs/cold_start_log.md` for a documented reproduction on a different machine.
