# Trading

TradingView Pine v6 indicators for Nifty / Sensex index options.

- `pine/strike_core.pine`: STRIKE CORE. Goes on the option chart (CE or PE). Two entry engines, one target, one stop.
- `pine/levels_suite.pine`: Levels Suite. Goes on the spot or index chart. Draws CPR, pivots, S/R, trendlines, VWAP and ORB. It gives no signals.

## Index gate (STRIKE CORE, settings group "Index gate")

Every entry now has to pass one read of the NIFTY regime. The read is computed the same way on the CE chart and the PE chart, so the two sides can't both be open for trading at the same time.

| Check | Default | What it blocks |
|---|---|---|
| Regime votes (VWAP, CPR, EMA 20/50, Supertrend, swing structure / trendline break) on the last closed 5m candle | 3 of 5 | CE unless BULL, PE unless BEAR, both when NEUTRAL |
| Regime must hold | 10 min | CE then PE within minutes on a flip-flop |
| ADX floor | 18 | Chop |
| Room to next index level ≥ k × "T1 needs" | 0.8 | Buying straight into R1, PDH, TC, VWAP and similar levels |
| Max stretch from regime EMA | 2 ATR | Buying the top of a spike |
| Skip first minutes | 15 | Opening noise |
| Cooldown after a stop | 20 min | Revenge re-entries |
| Stop for the day after | 2 stops | Bad days that keep getting worse |
| Strike Rate re-arm | always | Instant re-entry on the next bar after an SL while confluence stays latched |

When the gate blocks an entry, a grey ⊘ shows the reason. The Strike Check table has two new rows, **Index regime** and **Gate**. Untick "Gate entries on the index" to get the original behaviour back.
