# Position Memo: BNPL as a Leading Indicator of Consumer Credit Stress

**To:** Supervisory Policy Committee and bank Chief Risk Officers
**From:** Samruddhi Shrawne and Abhinav Sharaff
**Date:** October 28, 2026
**Re:** Including BNPL delinquency data in consumer credit early-warning dashboards

## Recommendation

Consumer credit early-warning dashboards that rely on credit card delinquency rates alone miss stress that shows up in Buy Now Pay Later data roughly 7 quarters earlier. Supervisory bodies and bank risk teams should treat BNPL 30+ day delinquency rates as a formal leading indicator alongside traditional credit card metrics. Affirm's 30+ DPD rate peaked in Q3 2022 at 3.83% while the Federal Reserve's bank-wide credit card 30+ DPD rate did not peak until Q2 2024 at 3.22%. Watching only credit card data gave the market nearly two years of false comfort while BNPL borrowers were already deteriorating.

## Evidence

The lead-lag relationship is visible in both the peaks and across the full series.

**Peak comparison.** Affirm Holdings is the largest pure-play US BNPL lender filing a 10-K and 10-Q with the SEC. Its 30+ day delinquency rate on loans held for investment, computed as the sum of the 30-59, 60-89, and 90-119 day buckets divided by total amortized cost basis, rose from 1.00% in Q4 2020 to 3.83% in Q3 2022 before falling back to 1.97% by Q2 2023. The Fed's DRCCLACBS series, which tracks 30+ day delinquency on credit card loans at all commercial banks, rose from 1.54% in Q2 2021 to 3.22% in Q2 2024. The gap between the two peaks is 7 quarters, or 21 months.

**Cross-correlation across the whole series.** The relationship holds beyond the peak pairs. Pearson correlation between Affirm 30+ DPD and credit card 30+ DPD across 24 quarters is -0.09 at zero lag and rises steadily to +0.76 at a lag of 8 quarters, where Affirm leads cards. The same correlation computed on quarter-over-quarter changes, which removes any shared drift, peaks at +0.62 at a 7 quarter lag. Two independent tests of lead-lag agree on the same offset.

**Economic rationale.** BNPL loans have shorter tenors than credit cards. Pay-in-four products settle in six weeks and installment loans run six months to a year. A stressed BNPL borrower reaches a delinquency bucket in weeks. A stressed credit card borrower may ride a revolving line for months before falling behind. The BNPL signal is mechanical, not predictive magic.

## Counterarguments and limitations

**Counterargument: different borrower pools.** The strongest objection is that BNPL customers skew younger, thinner-file, and lower-income than credit card holders, so the two series measure different populations under different stress. The point is fair. But the position does not require the two populations to be identical. It requires that stress in BNPL borrowers moves ahead of stress in bureau-reported borrowers, which the 7 to 8 quarter lead holds across both the levels test and the quarter-over-quarter changes test.

**Counterargument: Affirm now reports to credit bureaus.** Affirm began furnishing to Experian in April 2022, which weakens the simpler framing that BNPL is invisible to traditional data. The position still holds because furnishing to a bureau is not the same as entering standard credit scores at the same weight as a credit card trade line. Affirm's furnishing is also partial, delayed, and does not cover pay-in-four BNPL products at other issuers like Afterpay, Klarna, and PayPal.

**Biggest data limitation.** The analysis covers one credit cycle, 2020 Q2 to 2026 Q2. Cross-correlation on 24 quarters of overlapping observations has limited statistical power, and the signal largely measures how well two humps align. Because both series are strongly autocorrelated, the 24 quarters carry only about 7 independent pairs, so the adjusted 95% range on the peak correlation is wide (+0.03 to +0.96). Random look-alike series with the same autocorrelation match our best lag 5.4% of the time across 10,000 runs, just above the conventional 5% bar. A second cycle would materially strengthen or weaken the finding. We flag this honestly rather than overclaim the result as proven. The lead does survive every other robustness check we ran: prewhitened, year-over-year, 90+ day, drop-one-quarter, excluding 2020, and against card charge-offs.

**Why the position still holds despite the limitations.** Even if the lead-lag effect were weaker than measured, the asymmetric cost of ignoring BNPL is high. A 7-quarter lead that is directionally correct is more valuable than a 7-quarter lead that is precisely measured. Supervisory dashboards operate under uncertainty by design. Adding one more early signal is low cost. Removing it means waiting for the credit card series to confirm what BNPL already said.

## Now what

Three concrete steps for supervisory bodies and bank risk teams:

1. **Add BNPL 30+ DPD rates to consumer credit dashboards.** Affirm's data from its 10-K and 10-Q filings is public and quarterly. Block (Afterpay) and PayPal (Pay in 4) disclose less cleanly and should be requested in supervisory data calls.
2. **Treat BNPL delinquency moves of 50 basis points or more as a trigger for closer examination of card lending books.** In this sample the trigger first fired in Q4 2021, 10 quarters before the card peak, with one false alarm (Q2 2024). That is well over a year for card teams to adjust underwriting before the same trend reaches them.
3. **Fund longer time series collection.** The single-cycle finding is defensible but not definitive. The CFPB's 2022 and 2023 BNPL market reports and quarterly furnishing data from major BNPL issuers would support a cleaner test over the next cycle.

The headline chart is in `outputs/chart_lead_lag.png`, and the interactive dashboard (executive, analyst and regulator views) is in `dashboard/index.html`. Full data, scripts, and reproducibility steps are in the project repository at github.com/Samruddhi-Chetan-Shrawne/project-audible-bnpl.
