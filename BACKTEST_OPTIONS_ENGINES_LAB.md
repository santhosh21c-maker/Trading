# Options Engines Lab — Backtest Report

## Methodology (read this)

- **Period:** ~60 trading days of **5-minute** bars (Yahoo Finance), IST session 09:15–15:29.
- **Underlyings:** Nifty (`^NSEI`), BankNifty (`^NSEBANK`), Sensex (`^BSESN`).
- **Option series:** Yahoo does **not** provide NSE CE/PE OHLC. Premiums are **synthetic ATM proxies** (≈0.5 delta track + mild theta) so TP1=10 / SL=12 are tested in *premium points*, not index points.
- **Rules mirrored from** `Options_Engines_Lab.pine`: one engine at a time, TP1=10, TP2=20, TP3=35, SL=12, cooldown=5, max 6 entries/day, session + late-block + ADX chop filters, CE/PE sync via underlying EMA(9/21).
- **Same-bar SL vs TP:** if both could hit, **SL is prioritized** (conservative).
- This is a **relative ranking** of engines under one consistent model — not a guarantee of live NSE option PnL (IV crush, spreads, slippage not modeled).

## Headline numbers

| Metric | Value |
|--------|------:|
| Signal engines tested | 17 |
| Engines with **net profit** | **15** |
| Engines with **net loss** | **2** |
| Total trades (all engines × symbols × CE/PE) | 4932 |
| Profitable trades (PnL > 0) | 1640 (33.3%) |
| Losing trades | 3292 |
| **Stop-loss hits** | **2696** (54.7% of trades) |
| Exits by engine SELL | 1035 |
| Trades that tagged TP1 (+10) | 3491 |
| Trades that tagged TP2 (+20) | 2194 |
| Full exits at TP3 (+35) | 1201 |
| Combined net premium pts (sum of all engines)* | 10187.9 |

\*Combined net is **not** a realistic portfolio PnL (engines are alternatives, not run together). Use per-engine net below.

## Per-engine leaderboard (all symbols + CE/PE combined)

| Rank | Engine | Trades | Profit trades | Loss trades | SL hits | SL% | TP1 | TP2 | TP3 | Win% | Net pts | Avg pts |
|-----:|--------|-------:|--------------:|------------:|--------:|----:|----:|----:|----:|-----:|--------:|--------:|
| 1 | E14 Round Premium Levels | 1081 | 467 | 614 | 365 | 34% | 664 | 354 | 149 | 43% | 2350.4 | 2.17 |
| 2 | E3 VWAP Reclaim | 322 | 120 | 202 | 138 | 43% | 238 | 168 | 109 | 37% | 1853.5 | 5.76 |
| 3 | E7 ATR Expansion Impulse | 330 | 129 | 201 | 165 | 50% | 244 | 170 | 105 | 39% | 1637.1 | 4.96 |
| 4 | E5 Pullback Continuation | 403 | 123 | 280 | 225 | 56% | 290 | 190 | 108 | 31% | 820.9 | 2.04 |
| 5 | E8 RSI Regime | 248 | 75 | 173 | 118 | 48% | 173 | 114 | 67 | 30% | 715.6 | 2.89 |
| 6 | E1 Swing Structure | 334 | 99 | 235 | 230 | 69% | 240 | 164 | 98 | 30% | 660.4 | 1.98 |
| 7 | E6 EMA Stack Momentum | 614 | 169 | 445 | 443 | 72% | 461 | 296 | 168 | 28% | 555.5 | 0.90 |
| 8 | E21 Bollinger Squeeze Break | 38 | 16 | 22 | 16 | 42% | 30 | 20 | 16 | 42% | 324.4 | 8.54 |
| 9 | E13 Inside Bar Breakout | 185 | 57 | 128 | 118 | 64% | 136 | 81 | 48 | 31% | 293.4 | 1.59 |
| 10 | E9 MACD Histogram | 194 | 56 | 138 | 113 | 58% | 139 | 85 | 48 | 29% | 290.3 | 1.50 |
| 11 | E15 Option CPR / Pivot | 138 | 40 | 98 | 92 | 67% | 104 | 71 | 40 | 29% | 256.9 | 1.86 |
| 12 | E12 Rejection Wick Sweep | 161 | 51 | 110 | 90 | 56% | 122 | 73 | 37 | 32% | 254.2 | 1.58 |
| 13 | E11 Engulf + Volume | 215 | 65 | 150 | 119 | 55% | 155 | 96 | 48 | 30% | 240.8 | 1.12 |
| 14 | E10 Supertrend | 114 | 34 | 80 | 78 | 68% | 91 | 61 | 31 | 30% | 147.3 | 1.29 |
| 15 | E2 Opening Range Breakout | 138 | 36 | 102 | 97 | 70% | 99 | 65 | 34 | 26% | 8.1 | 0.06 |
| 16 | E4 Prev Day High/Low Break | 76 | 18 | 58 | 58 | 76% | 55 | 36 | 18 | 24% | -66.0 | -0.87 |
| 17 | E16 Donchian Channel Break | 341 | 85 | 256 | 231 | 68% | 250 | 150 | 77 | 25% | -155.0 | -0.45 |

## Profit vs Stop-Loss by engine

| Engine | Result | Net pts | SL hits | Profit trades |
|--------|--------|--------:|--------:|--------------:|
| E14 Round Premium Levels | ✅ PROFIT | 2350.4 | 365 | 467 |
| E3 VWAP Reclaim | ✅ PROFIT | 1853.5 | 138 | 120 |
| E7 ATR Expansion Impulse | ✅ PROFIT | 1637.1 | 165 | 129 |
| E5 Pullback Continuation | ✅ PROFIT | 820.9 | 225 | 123 |
| E8 RSI Regime | ✅ PROFIT | 715.6 | 118 | 75 |
| E1 Swing Structure | ✅ PROFIT | 660.4 | 230 | 99 |
| E6 EMA Stack Momentum | ✅ PROFIT | 555.5 | 443 | 169 |
| E21 Bollinger Squeeze Break | ✅ PROFIT | 324.4 | 16 | 16 |
| E13 Inside Bar Breakout | ✅ PROFIT | 293.4 | 118 | 57 |
| E9 MACD Histogram | ✅ PROFIT | 290.3 | 113 | 56 |
| E15 Option CPR / Pivot | ✅ PROFIT | 256.9 | 92 | 40 |
| E12 Rejection Wick Sweep | ✅ PROFIT | 254.2 | 90 | 51 |
| E11 Engulf + Volume | ✅ PROFIT | 240.8 | 119 | 65 |
| E10 Supertrend | ✅ PROFIT | 147.3 | 78 | 34 |
| E2 Opening Range Breakout | ✅ PROFIT | 8.1 | 97 | 36 |
| E4 Prev Day High/Low Break | ❌ LOSS | -66.0 | 58 | 18 |
| E16 Donchian Channel Break | ❌ LOSS | -155.0 | 231 | 85 |

## Takeaways

- **Best net engine:** E14 Round Premium Levels — net **2350.4** pts, SL hits 365/1081, TP1 tags 664.
- **Worst net engine:** E16 Donchian Channel Break — net **-155.0** pts, SL hits 231/341.
- **Most stop-outs:** E6 EMA Stack Momentum — **443** SL hits.
- **Most TP1 (+10) tags:** E14 Round Premium Levels — **664** times.
- Engines in profit: **15/17**. Engines in loss: **2/17**.

## Breakdown by underlying (net pts of each engine)

| engine                      |   BankNifty |   Nifty |   Sensex |
|:----------------------------|------------:|--------:|---------:|
| E1 Swing Structure          |       404   |  -254.6 |    511   |
| E10 Supertrend              |       155   |  -160.7 |    153   |
| E11 Engulf + Volume         |       178.2 |  -180.8 |    243.5 |
| E12 Rejection Wick Sweep    |       266.5 |   -58.8 |     46.5 |
| E13 Inside Bar Breakout     |        22.1 |    -5.7 |    277   |
| E14 Round Premium Levels    |      1274.5 |   -55.3 |   1131.2 |
| E15 Option CPR / Pivot      |        57   |    80.9 |    119   |
| E16 Donchian Channel Break  |       181   |  -364   |     28   |
| E2 Opening Range Breakout   |       129   |  -332.9 |    212   |
| E21 Bollinger Squeeze Break |       196   |    33.3 |     95.1 |
| E3 VWAP Reclaim             |       629.7 |   -25.5 |   1249.4 |
| E4 Prev Day High/Low Break  |       112   |  -159   |    -19   |
| E5 Pullback Continuation    |       360.3 |  -274.9 |    735.5 |
| E6 EMA Stack Momentum       |       448   |  -607.5 |    715   |
| E7 ATR Expansion Impulse    |       679.1 |   -54.8 |   1012.8 |
| E8 RSI Regime               |       262.8 |   -75   |    527.8 |
| E9 MACD Histogram           |       275   |  -189.2 |    204.5 |

## CE vs PE (net pts summed across underlyings)

| engine                      |     CE |     PE |
|:----------------------------|-------:|-------:|
| E1 Swing Structure          |  436.1 |  224.3 |
| E10 Supertrend              |  219.4 |  -72.1 |
| E11 Engulf + Volume         |  -56.2 |  297   |
| E12 Rejection Wick Sweep    | -108.3 |  362.4 |
| E13 Inside Bar Breakout     |   54.6 |  238.8 |
| E14 Round Premium Levels    |  949   | 1401.4 |
| E15 Option CPR / Pivot      |  201.5 |   55.3 |
| E16 Donchian Channel Break  |  236.2 | -391.2 |
| E2 Opening Range Breakout   |  101.8 |  -93.7 |
| E21 Bollinger Squeeze Break |  125.8 |  198.6 |
| E3 VWAP Reclaim             |  693.5 | 1160   |
| E4 Prev Day High/Low Break  |  168   | -234   |
| E5 Pullback Continuation    | -226.2 | 1047.1 |
| E6 EMA Stack Momentum       |  -89.7 |  645.2 |
| E7 ATR Expansion Impulse    |  646.3 |  990.8 |
| E8 RSI Regime               |  155.4 |  560.2 |
| E9 MACD Histogram           |  127.8 |  162.5 |

## Files

- `backtest_by_engine.csv` — engine aggregates
- `backtest_by_symbol_engine.csv` — per symbol/side
- `backtest_trades.csv` — every trade
- `backtest_options_engines_lab.py` — reproducible script
