# Smart Robotic Logic – Decider & Targets

Educational Pine Script recreation of **Decider** + **Target 1–4** levels (Nifty/Sensex option-style charts).

## Install

1. TradingView → **Pine Editor**
2. Paste `Smart_Robotic_Logic_Decider_Targets.pine`
3. **Add to chart** (CE/PE, 1m recommended)
4. Turn **Hybrid (Force 5 Min Values)** ON; set **Length** to 50

## Corrected model (important)

Earlier CPR (`TC`/`BC`) explanation for the Decider **gap** was wrong.

| Piece | Formula | Notes |
|--------|---------|--------|
| Centre **C** | Default `(H+L+C)/3` of Length window | Still a live hypothesis for the midpoint |
| Base **B** | Default `(H−L) × 0.382` (or ATR) | Equals Target-1 distance |
| **Decider** | `C ± 0.06·B` | Gap between lines = **0.12·B** (fixed fraction) |
| **Target N** | `C ± ratio·B` | Ratios **1 : 1.54 : 1.83 : 2.08** |

### Why not CPR?

CPR width = `(2C − H − L)/3` depends on where Close sits in the range and swings wildly as a % of range (~3–14% on real Nifty sessions). Your Decider gaps are a **fixed 0.12·B** on Call and Put — that only matches `C ± 0.06·B`.

Length 50→60 still changes levels because it changes the H/L/C window that feeds **C** and **B**.

## Tune if levels don't match live PxTrading

1. Switch **Centre C source** (Pivot / Close / HL2 / HLC3)
2. Adjust **Base B = Range ×** until Target 1 sits on the vendor’s Target 1
3. Leave Decider at `0.06` and Target ratios at `1 / 1.54 / 1.83 / 2.08` unless you measure otherwise
