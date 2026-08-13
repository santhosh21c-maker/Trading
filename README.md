# Trading — Pine tools

## Smart Robotic Logic (`Smart_Robotic_Logic_Decider_Targets.pine`)

Main Decider / Target indicator with **both segments**. Full math: **`HOW_LEVELS_ARE_PLOTTED.md`**.

| Segment | H/L source | Behaviour |
|---|---|---|
| **INDIAN - Index, Stock & Option** | Prior session day high/low (`Daily series` default) | Frozen from open. Extend = line length only. |
| **Robot Prediction** | Extend window (Auto OR-Last / Last / First / Offset) | LIVE. Extend changes levels. |

**Ladder (verified 12–13 Aug 2026 CALL/PUT):**
- `C = (H+L)/2`, `B = (H-L)/2`
- Decider = `C ± 0.06·B`
- Targets = `C ± {1.00, 1.54, 1.83, 2.08}·B` → Target 1 = H/L

Use on Nifty / BankNifty / Sensex **index, stock, or option** charts.

## Options Buy Decider Targets (`Options_Buy_Decider_Targets.pine`)

Simpler S/R-only variant (INDIAN / INTRADAY OR / PREDICTION). Prefer Smart Robotic for dual-segment work.

## Options Scalper 1-min (`Options_Scalper_1min.pine`)

1-min options scalper. Draws OR, day OHLC, and live trade Entry/Stop/T1–T3 only.

Educational only — not financial advice.
