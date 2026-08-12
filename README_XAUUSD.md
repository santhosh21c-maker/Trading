# XAUUSD Sweep + Fib Alpha

Educational Pine indicator inspired by **TW Alpha Sweep + Fib** style setups on Gold.

## What the screenshots show

| Chart | Entry | SL | TP1 | TP2 | TP3 | R |
|---|---|---|---|---|---|---|
| **1m** ACTIVE BUY | 4385.87 | 4382.37 | 4389.37 | 4392.87 | 4396.37 | **3.50** = Min SL |
| **5m** ACTIVE BUY | 4388.85 | 4384.04 | 4393.66 | 4398.47 | 4403.28 | **4.81** in 3.5..7 |

Same trade family, different execution TF → different Entry/SL/TP.  
TPs are always **1R / 2R / 3R**. Fib zone and 15m bias are shared filters.

## Inferred conditions (best effort)

### Always on
1. **15M Bias** — bullish for BUY, bearish for SELL  
2. **15M Fib zone** — swing strength 5, zone **0.512–0.60** → dashboard `FIB READY` after touch  
3. **Liquidity sweep** — lookback 10, equal H/L  
   - BUY needs **bear sweep** (wick below lows, reclaim)  
   - SELL needs **bull sweep** (wick above highs, reclaim)  
4. **Rejection** — confirmation candle after sweep (`Require Rejection`)  
5. **Risk** — structural distance to sweep extreme, **clamped to MinSL..MaxSL**  
   - Explains 1m R=3.5 (floor) vs 5m R=4.81 (structure)

### Why 1m ≠ 5m Entry/TP
- Fib + bias come from **15m** on both charts  
- Sweep / rejection / SL structure are measured on the **chart TF**  
- So 1m and 5m produce different Entry and R, then TP = Entry ± k·R

## Assumptions you can change in inputs
| Setting | Default assumption |
|---|---|
| Bias Mode | `Structure` from 15m pivots (also EMA / Mid) |
| Fib End | `0.600` (stream also showed 0.617 — switch if needed) |
| Entry | Signal candle **close** |
| SL | Beyond sweep extreme + buffer, clamped 3.5–7 |
| Equal HL tolerance | `$0.30` |
| One setup at a time | On |

## File
`XAUUSD_Sweep_Fib_Alpha.pine` — use on **XAUUSD 1m or 5m**.

Educational only — not financial advice / not a vendor copy.
