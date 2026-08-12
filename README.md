# Trading — Options Pine tools

## Options Buy Decider Targets (`Options_Buy_Decider_Targets.pine`)

Decider / Target 1–4 S/R for **Nifty / BankNifty / Sensex index, stock & option** charts.

### How Indian levels are plotted (matches PxTrading Smart Robotic Logic INDIAN)

1. Take **prior session day High / Low** of the chart symbol (`H`, `L`).
2. `C = (H+L)/2`, `B = (H-L)/2`
3. **Decider** = `C ± 0.06·B`
4. **Targets** = `C ± {1.00, 1.54, 1.83, 2.08}·B`  
   → Target 1 High/Low equals prior-day `H`/`L`
5. Levels **freeze from the open** (available before 09:50 — not an opening-range freeze).

**Mode default:** `INDIAN Daily Prior HL` (optional Hybrid Force 5m).  
Also supports `INTRADAY OR Freeze` and `PREDICTION Lookback`.

Verified against 12 Aug 2026 CALL/PUT 24500 screenshot values.

## Options Scalper 1-min (`Options_Scalper_1min.pine`)

Use on option premium charts (1-minute). Draws OR high/low, day OHLC, and live trade Entry/Stop/T1–T3 only.

## Smart Robotic Logic (`Smart_Robotic_Logic_Decider_Targets.pine`)

Educational recreation with **INDIAN** (prior-day freeze) and **Robot Prediction** segments.

Educational only — not financial advice.
