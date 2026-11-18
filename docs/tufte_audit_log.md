# Tufte Audit Log

**Project Audible · FINTECH 590.05 · Fall 2026**

Every visual in the dashboard and the static headline chart, checked against the five Lecture 12 tests: data-ink, chartjunk, lie factor, graphical integrity and data density. ✓ = passed as found, ✗ = failed as found, then fixed in the "Change made" column. Lie factor is the size of the effect shown divided by the size of the effect in the data (Tufte's tolerance is 0.95 to 1.05). Every length or position axis below starts at zero and is linear, so the lie factor is 1.0 unless a row says otherwise.

Pre-filled by Abhinav Sharaff (dashboard author). The lecture requires a peer audit, so Samruddhi Shrawne reviews each row and signs below. Any row she disagrees with gets changed before the defense.

| Visual | Page | Ink | Junk | Lie | Integ. | Density | Change made |
|---|---|---|---|---|---|---|---|
| V-01 Conclusion card (7 quarters, peaks, trigger status) | Executive | ✓ | ✓ | n/a (number) | ✓ | ✓ | Headline restated for the reframed position: saving rate first, Affirm confirms, cards 7 quarters after Affirm (PR #9) |
| V-02 Affirm vs card 30+ DPD, quarterly | Executive | ✓ | ✓ | ✓ 1.0 | ✗ | ✓ | Added as-of stamp to the subtitle. Peaks labeled directly; trigger quarters lightly shaded |
| V-03 Personal saving rate, quarterly | Executive | ✓ | ✓ | ✓ 1.0 | ✗ | ✓ | Built as a separate chart on its own axis, not a second y-axis on V-02 (PR #7). Added as-of stamp. Single series, so no legend |
| V-04 Trigger status chip | Executive | ✓ | ✓ | n/a | ✓ | ✓ | None. Status shown by icon and text, not color alone |
| V-05 Leading series shifted against cards | Risk | ✓ | ✓ | ✓ 1.0 | ✓ | ✓ | None. Different units go on stacked panels, never a dual axis. The saving rate plots on a flipped axis (lower rate plots higher), labeled in the axis title and the subtitle. Window shown in the subtitle |
| V-06 Correlation by lag, with adjusted 95% CI | Risk | ✓ | ✓ | ✓ 1.0 | ✗ | ✓ | Added as-of stamp. Fixed −1 to +1 axis with a zero line (never auto-scaled). Pairs and effective pairs printed under each bar |
| V-07 Affirm 30+ DPD balances, $M | Risk | ✓ | ✓ | ✓ 1.0 | ✗ | ✓ | Added as-of stamp. Bars start at zero; the peak quarter is highlighted, the rest muted |
| V-08 Peaks/troughs and trigger history tables | Risk | ✓ | ✓ | n/a | ✓ | ✓ | None |
| V-09 Position ledger (14 checks) | Risk | ✓ | ✓ | n/a | ✓ | ✓ | None. Verdicts shown by icon and word, not color alone |
| V-10 Reported 30+ DPD with reporting changes marked | Compliance | ✓ | ✓ | ✓ 1.0 | ✗ | ✓ | Added as-of stamp. Basis changes and Experian reporting date marked on the chart |
| V-11 Headline figures and how each is reproduced | Compliance | ✓ | ✓ | n/a | ✓ | ✓ | Added a fact-ledger ID column (F-01 to F-20) and rows for the saving-rate and trigger figures, so every Executive-page number traces to a ledger row |
| V-12 Source register, one row per quarter | Compliance | ✓ | ✓ | n/a | ✓ | ✓ | Added saving-rate column (PR #7) |
| V-13 Quarter drill-through: context chart and tiles | Drill-through | ✓ | ✓ | ✓ 1.0 | ✓ | ✓ | None. Selected quarter marked with a line; quarter named in the title |
| V-14 Lag drill-through: scatter of quarter pairs | Drill-through | ✓ | ✓ | n/a (position, no zero needed for a scatter) | ✓ | ✓ | None. Window and effective pairs in the subtitle |
| V-15 outputs/chart_lead_lag.png (static headline chart) | Repo / memo | ✓ | ✓ | ✓ 1.0 | ✗ | ✓ | Colors were the reverse of the dashboard (Affirm blue, cards orange); swapped to match. Title said "BNPL delinquencies"; now "Affirm delinquency". Quarter labels changed to "Q3 2022" format. Added data-through and pull date |

## Open items

- **Ledger IDs in tooltips (Lecture 12, "turn on"). Closed Nov 18.** V-11 now carries an ID column, each figure's drill-through names its ledger row, and hovering a labeled peak, trigger or saving-rate label on the Executive charts shows its ID.
- **Panel cards.** Each visual sits on a white card with a 1 px border. This is page layout, not chart ink, so we kept it.

## Peer sign-off

Audited by Samruddhi Shrawne: Samruddhi Shrawne       Date: 2026-11-18
