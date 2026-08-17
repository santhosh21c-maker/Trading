# Trading — Pine tools

## Smart Robotic Logic (`Smart_Robotic_Logic_Decider_Targets.pine`)

Main Decider / Target indicator with **both segments**. Full math: **`HOW_LEVELS_ARE_PLOTTED.md`**.

| Segment | Default anchors | Behaviour |
|---|---|---|
| **INDIAN** | **Prev Close + Prev Low (Daily)** on index (corrected 14 Aug 2026 test) | Frozen from open. Extend = line length only. |
| **Robot Prediction** | Extend window High/Low | LIVE. Extend changes levels. |

**Ladder algebra (verified):**
- `C = (H+L)/2`, `B = (H-L)/2`
- Decider = `C ± 0.06·B`
- Targets = `C ± {1.00, 1.54, 1.83, 2.08}·B`

**Important:** Target 1 *labels* are the anchors H/L. That does not by itself prove what session statistic produced them. On Nifty **index** 14 Aug 2026, anchors matched **prior Close/Low**, not prior High/Low. See `HOW_LEVELS_ARE_PLOTTED.md`.

## Options Buy Decider Targets (`Options_Buy_Decider_Targets.pine`)

Simpler S/R-only variant. Prefer Smart Robotic for dual-segment work.

## Options Scalper 1-min (`Options_Scalper_1min.pine`)

1-min options scalper. Educational only — not financial advice.
