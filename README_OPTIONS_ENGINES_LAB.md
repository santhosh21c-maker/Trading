# Options Engines Lab · CE/PE (v1.0)

Paste `Options_Engines_Lab.pine` on a **Nifty / BankNifty / Sensex option** chart (1m, 3m, or 5m).

## Defaults
| | Pts (premium) |
|--|--|
| TP1 | **10** |
| TP2 | **20** |
| TP3 | **35** |
| SL | 12 fixed (or swing+buffer) |

## Use
1. Settings → **Active engine** (one at a time).
2. Green candles = in BUY · Red = flat / after SELL exit.
3. **CE/PE sync ON**: BUY only on CE when underlying bullish, only on PE when bearish.
4. Dashboard shows today’s trades, TP hits, net pts — switch engines and compare.

## Engines
E1–E16 + E21 = signal engines · E17–E19 filters · E20 sync · E22 dashboard.
