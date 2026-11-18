# Cold-Start Log

**Project Audible · FINTECH 590.05 · Fall 2026**

The test: fresh clone from GitHub, one command, no manual steps, exit 0, and the same numbers as the committed dashboard. `run_demo.sh` was written by Samruddhi Shrawne; this run was done by Abhinav Sharaff on a different machine.

## Run 2 (pass)

| | |
|---|---|
| Date | November 17, 2026, 9:49 PM ET (2026-11-18 02:49 UTC) |
| Run by | Abhinav Sharaff |
| Machine | macOS 26.6.2, Apple silicon (arm64) |
| Python | 3.13.5, python.org installer, no certificate setup |
| Code | Fresh clone of branch `fred-ssl` at `79680c7` (main plus the fix below) |
| Command | `./run_demo.sh` (full run: live FRED and SEC EDGAR pulls) |
| Result | **Exit code 0, 98 seconds** |

**Outputs match the committed dashboard.** Compared to `dashboard/data.js` on main: every quarterly value, the KPIs, all 14 ledger results and the trigger history are identical. Headline figures reproduced: Affirm peak 3.83% (Q3 2022), card peak 3.22% (Q2 2024), 7 quarters apart; r = 0.761 at an 8-quarter lead (n = 16) in levels and r = 0.622 at a 7-quarter lead (n = 15) in changes; null p = 0.054.

**Differences from the frozen pull, none inside the analysis window:**
- The live SEC pull found 86 filings (83 on Oct 26) and added Affirm's Q3 2026 row (30+ DPD 2.947%, from the 10-Q filed Nov 5, accession 0001628280-26-071153). It is outside the Q2 2020 to Q2 2026 window, so no figure changes.
- Q2 2026 is now sourced from that 10-Q's comparative column instead of the 10-K, at the same value (2.509%).
- FRED has revised REVOLSL and TOTALSL since Oct 26. The three series the analysis uses (DRCCLACBS, CORCCACBS, PSAVERT) are unchanged.

## Run 1 (fail, fixed)

Same machine, fresh clone of main at `99ac0d9`. Exit code 1 after 74 seconds: `pull_fred.py` failed with `SSL: CERTIFICATE_VERIFY_FAILED`. It downloaded with `urllib`, which uses the system certificate store, and a fresh python.org install on macOS has none until a setup script is run. Fix: download with `requests` (already in `requirements.txt`), which bundles its own certificates. This is the kind of failure a cold start exists to catch; it did not show up on the machines where the pipeline was developed.

## Partner sign-off

Reviewed by Samruddhi Shrawne: Samruddhi Shrawne       Date: 2026-11-18

## Full output, run 2

```
# Cold-start run
date: 2026-11-18 02:49 UTC
machine: macOS 26.6.2, arm64
python3: Python 3.13.5 (python.org installer, no certificate setup)
commit: 79680c7 (fresh clone of origin/fred-ssl = main + FRED SSL fix)
command: ./run_demo.sh (full run, live FRED and SEC EDGAR pulls)
---
==> [1/3] Creating clean environment (.venv)
==> [2/3] Running pipeline
Pulling FRED series...
  DRCCLACBS: 30 rows, 2019-01-01 to 2026-04-01
  CORCCACBS: 30 rows, 2019-01-01 to 2026-04-01
  PSAVERT: 90 rows, 2019-01-01 to 2026-06-01
  REVOLSL: 90 rows, 2019-01-01 to 2026-06-01
  TOTALSL: 90 rows, 2019-01-01 to 2026-06-01

Aggregating to quarterly...

Wrote data/processed/fred_quarterly.csv: 30 quarters, 5 series
   quarter  cc_30plus_dpd_rate_pct  cc_nco_rate_pct  personal_savings_rate_pct  revolving_consumer_credit_bil  total_consumer_credit_bil
2024-09-30                    3.20             4.69                   6.033333                     1342480.89                 5058345.12
2024-12-31                    3.08             4.57                   5.533333                     1296965.62                 4947229.57
2025-03-31                    3.05             4.44                   5.700000                     1292802.44                 5021864.14
2025-06-30                    3.04             4.19                   5.800000                     1301742.11                 5043533.78
2025-09-30                    2.99             4.18                   5.200000                     1312713.57                 5071963.43
2025-12-31                    2.95             4.09                   4.933333                     1324322.29                 5098820.78
2026-03-31                    2.91             3.82                   5.333333                     1338182.22                 5131428.88
2026-06-30                    2.85             3.82                   4.400000                     1354418.69                 5170754.93
Fetching EDGAR submissions for AFRM (CIK 0001820953)...
Found 86 filings of type {'8-K', '10-K', '10-Q'} since 2021
  [1/86] 2026-11-05 10-Q (afrm-20260930.htm)... downloaded
  [2/86] 2026-11-05 8-K (afrm-20261105.htm)... downloaded
  [3/86] 2026-08-27 10-K (afrm-20260630.htm)... downloaded
  [4/86] 2026-08-27 8-K (afrm-20260825.htm)... downloaded
  [5/86] 2026-06-25 8-K (afrm-20260618.htm)... downloaded
  [6/86] 2026-05-07 10-Q (afrm-20260331.htm)... downloaded
  [7/86] 2026-05-07 8-K (afrm-20260507.htm)... downloaded
  [8/86] 2026-02-05 10-Q (afrm-20251231.htm)... downloaded
  [9/86] 2026-02-05 8-K (afrm-20260205.htm)... downloaded
  [10/86] 2026-01-16 8-K (afrm-20260113.htm)... downloaded
  [11/86] 2025-12-18 8-K (afrm-20251215.htm)... downloaded
  [12/86] 2025-11-06 10-Q (afrm-20250930.htm)... downloaded
  [13/86] 2025-11-06 8-K (afrm-20251102.htm)... downloaded
  [14/86] 2025-09-22 8-K (afrm-20250918.htm)... downloaded
  [15/86] 2025-08-28 10-K (afrm-20250630.htm)... downloaded
  [16/86] 2025-08-28 8-K (afrm-20250828.htm)... downloaded
  [17/86] 2025-06-26 8-K (afrm-20250625.htm)... downloaded
  [18/86] 2025-06-12 8-K (afrm-20250609.htm)... downloaded
  [19/86] 2025-05-09 10-Q (afrm-20250331.htm)... downloaded
  [20/86] 2025-05-08 8-K (afrm-20250508.htm)... downloaded
  [21/86] 2025-03-17 8-K (afrm-20250317.htm)... downloaded
  [22/86] 2025-02-28 8-K (afrm-20250228.htm)... downloaded
  [23/86] 2025-02-20 8-K (afrm-20250214.htm)... downloaded
  [24/86] 2025-02-06 10-Q (afrm-20241231.htm)... downloaded
  [25/86] 2025-02-06 8-K (afrm-20250206.htm)... downloaded
  [26/86] 2024-12-20 8-K (afrm-20241220.htm)... downloaded
  [27/86] 2024-12-18 8-K (afrm-20241217.htm)... downloaded
  [28/86] 2024-12-16 8-K (afrm-20241216.htm)... downloaded
  [29/86] 2024-12-12 8-K (afrm-20241209.htm)... downloaded
  [30/86] 2024-11-07 10-Q (afrm-20240930.htm)... downloaded
  [31/86] 2024-11-07 8-K (afrm-20241105.htm)... downloaded
  [32/86] 2024-08-28 10-K (afrm-20240630.htm)... downloaded
  [33/86] 2024-08-28 8-K (afrm-20240828.htm)... downloaded
  [34/86] 2024-07-01 8-K (afrm-20240625.htm)... downloaded
  [35/86] 2024-06-20 8-K (afrm-20240617.htm)... downloaded
  [36/86] 2024-06-11 8-K (afrm-20240611.htm)... downloaded
  [37/86] 2024-05-08 10-Q (afrm-20240331.htm)... downloaded
  [38/86] 2024-05-08 8-K (afrm-20240508.htm)... downloaded
  [39/86] 2024-02-08 10-Q (afrm-20231231.htm)... downloaded
  [40/86] 2024-02-08 8-K (afrm-20240208.htm)... downloaded
  [41/86] 2023-12-08 8-K (afrm-20231204.htm)... downloaded
  [42/86] 2023-11-08 10-Q (afrm-20230930.htm)... downloaded
  [43/86] 2023-11-08 8-K (afrm-20231108.htm)... downloaded
  [44/86] 2023-10-20 8-K (afrm-20231017.htm)... downloaded
  [45/86] 2023-08-25 10-K (afrm-20230630.htm)... downloaded
  [46/86] 2023-08-24 8-K (afrm-20230824.htm)... downloaded
  [47/86] 2023-06-08 8-K (afrm-20230607.htm)... downloaded
  [48/86] 2023-05-09 10-Q (afrm-20230331.htm)... downloaded
  [49/86] 2023-05-09 8-K (afrm-20230509.htm)... downloaded
  [50/86] 2023-03-07 8-K (afrm-20230306.htm)... downloaded
  [51/86] 2023-02-15 8-K (afrm-20230214.htm)... downloaded
  [52/86] 2023-02-08 10-Q (afrm-20221231.htm)... downloaded
  [53/86] 2023-02-08 8-K (afrm-20230208.htm)... downloaded
  [54/86] 2022-12-09 8-K (afrm-20221205.htm)... downloaded
  [55/86] 2022-11-08 10-Q (afrm-20220930.htm)... downloaded
  [56/86] 2022-11-08 8-K (afrm-20221108.htm)... downloaded
  [57/86] 2022-09-22 8-K (afrm-20220916.htm)... downloaded
  [58/86] 2022-08-29 10-K (afrm-20220630.htm)... downloaded
  [59/86] 2022-08-25 8-K (afrm-20220823.htm)... downloaded
  [60/86] 2022-06-06 8-K (afrm-20220531.htm)... downloaded
  [61/86] 2022-05-13 10-Q (afrm-20220331.htm)... downloaded
  [62/86] 2022-05-12 8-K (afrm-20220512.htm)... downloaded
  [63/86] 2022-03-14 8-K (afrm-20220314.htm)... downloaded
  [64/86] 2022-03-03 8-K (afrm-20220303.htm)... downloaded
  [65/86] 2022-02-14 10-Q (afrm-20211231.htm)... downloaded
  [66/86] 2022-02-10 8-K (afrm-20220210.htm)... downloaded
  [67/86] 2021-12-13 8-K (afrm-20211210.htm)... downloaded
  [68/86] 2021-12-07 8-K (afrm-20211203.htm)... downloaded
  [69/86] 2021-11-23 8-K (tm2133732d1_8k.htm)... downloaded
  [70/86] 2021-11-19 8-K (tm2133447d1_8k.htm)... downloaded
  [71/86] 2021-11-18 8-K (tm2133226d1_8k.htm)... downloaded
  [72/86] 2021-11-15 10-Q (afrm-20210930.htm)... downloaded
  [73/86] 2021-11-10 8-K (afrm-20211110.htm)... downloaded
  [74/86] 2021-10-20 8-K (afrm-20211015.htm)... downloaded
  [75/86] 2021-09-17 10-K (afrm-20210630.htm)... downloaded
  [76/86] 2021-09-09 8-K (afrm-20210909.htm)... downloaded
  [77/86] 2021-09-08 8-K (afrm-20210902.htm)... downloaded
  [78/86] 2021-08-30 8-K (tm2126423d1_8k.htm)... downloaded
  [79/86] 2021-05-17 10-Q (afrm-20210331.htm)... downloaded
  [80/86] 2021-05-10 8-K (afrm-20210508.htm)... downloaded
  [81/86] 2021-04-22 8-K (afrm-20210420.htm)... downloaded
  [82/86] 2021-03-10 8-K (afrm-20210304.htm)... downloaded
  [83/86] 2021-02-17 10-Q (afrm-20201231.htm)... downloaded
  [84/86] 2021-02-11 8-K (afrm-20210211.htm)... downloaded
  [85/86] 2021-01-25 8-K (a21-3836_18k.htm)... downloaded
  [86/86] 2021-01-15 8-K (a20-26663_248k.htm)... downloaded

Wrote data/raw/affirm/affirm_filings_index.csv: 86 rows

Filings to use for delinquency data: all 10-Q and 10-K entries.
Open each, locate the 'Delinquency' or 'Credit Quality' table, type
the 30+ DPD rate into affirm_delinquency_raw.csv.
  10-Q 2026-09-30 0001628280-26-071153: [('2026-09-30', 'hfi_by_origination'), ('2026-06-30', 'hfi_by_origination')]
  10-K 2026-06-30 0001628280-26-059279: [('2026-06-30', 'hfi_by_origination'), ('2025-06-30', 'hfi_by_origination')]
  10-Q 2026-03-31 0001628280-26-032294: [('2026-03-31', 'hfi_by_origination'), ('2025-06-30', 'hfi_by_origination')]
  10-Q 2025-12-31 0001628280-26-005855: [('2025-12-31', 'hfi_by_origination'), ('2025-06-30', 'hfi_by_origination')]
  10-Q 2025-09-30 0001628280-25-050295: [('2025-09-30', 'hfi_by_origination'), ('2025-06-30', 'hfi_by_origination')]
  10-K 2025-06-30 0001820953-25-000080: [('2025-06-30', 'hfi'), ('2024-06-30', 'hfi')]
  10-Q 2025-03-31 0001820953-25-000052: [('2025-03-31', 'hfi_hfs'), ('2024-06-30', 'hfi_hfs')]
  10-Q 2024-12-31 0001820953-25-000012: [('2024-12-31', 'hfi_hfs'), ('2024-06-30', 'hfi_hfs')]
  10-Q 2024-09-30 0001820953-24-000060: [('2024-09-30', 'hfi_hfs'), ('2024-06-30', 'hfi_hfs')]
  10-K 2024-06-30 0001820953-24-000035: [('2024-06-30', 'hfi_hfs'), ('2023-06-30', 'hfi_hfs')]
  10-Q 2024-03-31 0001820953-24-000014: [('2024-03-31', 'hfi_hfs'), ('2023-06-30', 'hfi_hfs')]
  10-Q 2023-12-31 0001820953-24-000006: [('2023-12-31', 'hfi_hfs'), ('2023-06-30', 'hfi_hfs')]
  10-Q 2023-09-30 0001820953-23-000025: [('2023-09-30', 'hfi_hfs'), ('2023-06-30', 'hfi_hfs')]
  10-K 2023-06-30 0001820953-23-000016: [('2023-06-30', 'hfi_hfs'), ('2022-06-30', 'hfi_hfs')]
  10-Q 2023-03-31 0001820953-23-000013: [('2023-03-31', 'hfi_hfs'), ('2022-06-30', 'hfi_hfs')]
  10-Q 2022-12-31 0001820953-23-000002: [('2022-12-31', 'hfi_hfs'), ('2022-06-30', 'hfi_hfs')]
  10-Q 2022-09-30 0001820953-22-000039: [('2022-09-30', 'hfi_hfs'), ('2022-06-30', 'hfi_hfs')]
  10-K 2022-06-30 0001628280-22-023828: [('2022-06-30', 'hfi_hfs'), ('2021-06-30', 'hfi_hfs')]
  10-Q 2022-03-31 0001820953-22-000031: [('2022-03-31', 'hfi_hfs'), ('2021-06-30', 'hfi_hfs')]
  10-Q 2021-12-31 0001820953-22-000005: [('2021-12-31', 'hfi_hfs'), ('2021-06-30', 'hfi_hfs')]
  10-Q 2021-09-30 0001820953-21-000117: [('2021-09-30', 'hfi'), ('2021-06-30', 'hfi')]
  10-K 2021-06-30 0001820953-21-000102: [('2021-06-30', 'hfi'), ('2020-06-30', 'hfi')]
  10-Q 2021-03-31 0001628280-21-010407: [('2020-06-30', 'hfi'), ('2021-03-31', 'hfi')]
  10-Q 2020-12-31 0001628280-21-002353: [('2020-06-30', 'hfi_hfs_upb'), ('2020-12-31', 'hfi_hfs_upb')]

Wrote data/processed/affirm_quarterly.csv: 25 quarters
quarter_end  delinquency_30plus_pct  delinquency_90plus_pct  loans_held_for_investment_mil              basis     source_accession
 2020-06-30                  1.6906                  0.5843                       1054.077                hfi 0001820953-21-000102
 2020-12-31                  1.0021                  0.2676                       1953.610        hfi_hfs_upb 0001628280-21-002353
 2021-03-31                  1.3840                  0.3420                       2193.934                hfi 0001628280-21-010407
 2021-06-30                  1.7857                  0.3346                       2019.884            hfi_hfs 0001628280-22-023828
 2021-09-30                  2.5953                  0.6195                       2229.817                hfi 0001820953-21-000117
 2021-12-31                  3.4633                  0.9019                       2433.340            hfi_hfs 0001820953-22-000005
 2022-03-31                  3.7172                  1.1548                       2486.088            hfi_hfs 0001820953-22-000031
 2022-06-30                  3.4058                  0.9279                       2485.534            hfi_hfs 0001820953-23-000016
 2022-09-30                  3.8293                  1.0580                       2665.384            hfi_hfs 0001820953-22-000039
 2022-12-31                  2.6832                  0.8004                       3622.993            hfi_hfs 0001820953-23-000002
 2023-03-31                  2.2946                  0.6782                       3741.716            hfi_hfs 0001820953-23-000013
 2023-06-30                  1.9679                  0.4876                       4361.965            hfi_hfs 0001820953-24-000035
 2023-09-30                  2.4719                  0.6682                       4502.391            hfi_hfs 0001820953-23-000025
 2023-12-31                  2.4749                  0.7110                       5183.363            hfi_hfs 0001820953-24-000006
 2024-03-31                  2.2467                  0.6533                       5401.075            hfi_hfs 0001820953-24-000014
 2024-06-30                  2.5217                  0.6887                       5607.296                hfi 0001820953-25-000080
 2024-09-30                  2.7196                  0.7664                       6238.327            hfi_hfs 0001820953-24-000060
 2024-12-31                  2.7217                  0.7875                       6720.071            hfi_hfs 0001820953-25-000012
 2025-03-31                  2.6474                  0.7515                       6561.450            hfi_hfs 0001820953-25-000052
 2025-06-30                  2.4622                  0.6860                       6957.582 hfi_by_origination 0001628280-26-059279
 2025-09-30                  2.8819                  0.8078                       7161.307 hfi_by_origination 0001628280-25-050295
 2025-12-31                  2.6331                  0.7876                       8684.255 hfi_by_origination 0001628280-26-005855
 2026-03-31                  2.7854                  0.7609                       8483.593 hfi_by_origination 0001628280-26-032294
 2026-06-30                  2.5089                  0.6749                       9466.383 hfi_by_origination 0001628280-26-071153
 2026-09-30                  2.9470                  0.7827                      10010.781 hfi_by_origination 0001628280-26-071153
Affirm peak:      2022 Q3 (2022-09-30) at 3.83%
Credit card peak: 2024 Q2 (2024-06-30) at 3.22%
Quarters between peaks: 7 (1.75 years)

Wrote outputs/chart_lead_lag.png
 lag_q  r_levels  n_levels  r_changes  n_changes
     0    -0.093        24     -0.357         22
     1    +0.081        23     -0.321         21
     2    +0.200        22     -0.234         20
     3    +0.336        21     +0.060         19
     4    +0.456        20     +0.191         18
     5    +0.566        19     +0.289         17
     6    +0.665        18     +0.486         16
     7    +0.738        17     +0.622         15
     8    +0.761        16     +0.621         14
     9    +0.717        15     +0.444         13
    10    +0.578        14     +0.453         12

Levels:  max r = +0.761 at lag 8 (n = 16)
Changes: max r = +0.622 at lag 7 (n = 15)
Wrote dashboard/data.js: 25 quarters, lead = 7 quarters, best r = 0.761 at lag 8, 2 trigger episodes (1 unconfirmed)
  n_eff = 7.1, adjusted CI 0.031 to 0.962; null p = 0.054; leads across checks 7-8 quarters
==> [3/3] Done
Open this file in a browser (it runs offline, Plotly is vendored):
    <clone>/dashboard/index.html
Headline chart: <clone>/outputs/chart_lead_lag.png
---
exit code: 0; elapsed: 98s
```
