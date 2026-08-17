# Nifty Multi-Strike Backtest — Options Confluence (3 CE + 3 PE × 2 expiries)

## Scope

- **3 Calls + 3 Puts** per expiry (ITM / ATM / OTM around ATM)
- **Expiries:** 2025-06-26 and 2025-07-31 (NSE archive; Aug-2026 chain unavailable here)
- **Strategy:** Nifty Options Confluence — min **3** engines, TP **10/20/35**, SL **10**, TP1→BE, CE/PE sync
- **1h paths:** Nifty 1h spot + **per-strike IV** fit to that day’s **real NSE option close**
- **Daily check:** real NSE OHLC also saved (Jul PE printed TP3; CE had no daily confluence entries)

## Headline (1h, both expiries)

| Metric | Value |
|--------|------:|
| Strike-contracts tested | 12 (6 per expiry × 2) |
| Total trades | 66 |
| Profitable trades | 42 |
| Losing trades | 24 |
| **Stop-loss hits** | **23** |
| BE/trail exits | 38 |
| TP3 exits | 4 |
| Confluence SELL | 1 |
| TP1 tags | 42 |
| **Combined net pts** | **115.0** |
| CE net | 15.0 |
| PE net | 100.0 |
| Contracts net profit | **6 / 12** |
| Contracts net loss | **6 / 12** |

## Per strike × expiry (1h IV-calibrated)

| Expiry | Side | Strike | Type | Trades | Wins | Losses | SL | BE/trail | TP3 | Sell | TP1 | Win% | Net | Avg | Best | Worst |
|--------|------|-------:|------|-------:|-----:|-------:|---:|---------:|----:|-----:|----:|-----:|----:|----:|------:|------:|
| 2025-06-26 | CE | 24650 | ITM | 6 | 5 | 1 | 1 | 5 | 0 | 0 | 5 | 83.3 | 25.0 | 4.17 | 7.5 | -10.0 |
| 2025-06-26 | CE | 24750 | ATM | 6 | 5 | 1 | 1 | 5 | 0 | 0 | 5 | 83.3 | 22.5 | 3.75 | 7.5 | -10.0 |
| 2025-06-26 | CE | 24850 | OTM | 6 | 5 | 1 | 1 | 5 | 0 | 0 | 5 | 83.3 | 22.5 | 3.75 | 7.5 | -10.0 |
| 2025-06-26 | PE | 24650 | OTM | 5 | 2 | 3 | 3 | 2 | 0 | 0 | 2 | 40.0 | -15.0 | -3.0 | 7.5 | -10.0 |
| 2025-06-26 | PE | 24750 | ATM | 5 | 2 | 3 | 3 | 2 | 0 | 0 | 2 | 40.0 | -15.0 | -3.0 | 7.5 | -10.0 |
| 2025-06-26 | PE | 24850 | ITM | 5 | 2 | 3 | 3 | 2 | 0 | 0 | 2 | 40.0 | -15.0 | -3.0 | 7.5 | -10.0 |
| 2025-07-31 | CE | 25350 | ITM | 6 | 2 | 4 | 3 | 2 | 0 | 1 | 2 | 33.3 | -20.01 | -3.33 | 7.5 | -10.0 |
| 2025-07-31 | CE | 25450 | ATM | 5 | 2 | 3 | 3 | 2 | 0 | 0 | 2 | 40.0 | -17.5 | -3.5 | 7.5 | -10.0 |
| 2025-07-31 | CE | 25550 | OTM | 5 | 2 | 3 | 3 | 2 | 0 | 0 | 2 | 40.0 | -17.5 | -3.5 | 7.5 | -10.0 |
| 2025-07-31 | PE | 25350 | OTM | 5 | 5 | 0 | 0 | 3 | 2 | 0 | 5 | 100.0 | 65.0 | 13.0 | 22.5 | 5.0 |
| 2025-07-31 | PE | 25450 | ATM | 6 | 5 | 1 | 1 | 4 | 1 | 0 | 5 | 83.3 | 37.5 | 6.25 | 22.5 | -10.0 |
| 2025-07-31 | PE | 25550 | ITM | 6 | 5 | 1 | 1 | 4 | 1 | 0 | 5 | 83.3 | 42.5 | 7.08 | 22.5 | -10.0 |

## By side (combined)

| Side | Trades | Wins | SL hits | Net pts |
|------|-------:|-----:|--------:|--------:|
| CE | 34 | 21 | 12 | 15.0 |
| PE | 32 | 21 | 11 | 100.0 |

## Takeaways

- You now have **detailed numbers on 3 CE + 3 PE strikes** (×2 monthly expiries).
- **PE outperformed CE** in Jul-2025 (index sold off into expiry; CE→~0.1). Side sync did its job (no fighting the trend).
- **SL hits** are the main loss source on CE; PE used more **BE/trail** and **TP3**.
- Prefer **ATM / 100-pt ITM** for liquidity; OTM still worked on PE in the selloff but is riskier live.
- Live: run `Nifty_Options_Confluence.pine` on the **exact CE/PE chart** you trade (3m/5m).

## Files

- `BACKTEST_MULTISTRIKE_NIFTY.md` (this report)
- `BACKTEST_MULTISTRIKE_SUMMARY_2EXP.csv`
- `BACKTEST_MULTISTRIKE_TRADES_2EXP.csv`
- `nifty_opt_daily_*.csv` (Jul real NSE daily)