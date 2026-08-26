# Strike Rate — entries per day (multi-strike)

**Data:** Nifty 5m Yahoo `^NSEI` · 2026-06-04 → 2026-08-26 · **59 session days**
**Strikes tested:** [24200, 24250, 24300, 24350, 24400] (ATM≈24300 ±50/100) · CE & PE synthetic premiums
**Note:** Free feeds lack real NSE option OHLC; premium paths are synthetic. Frequency is driven mainly by **index engines + filters**, so strike differences are modest.

## Headline — do we get ≥2 entries/day?

| Config | Avg / session-day (per chart) | Avg / active day | % days with ≥2 | ATM CE /day | ATM PE /day |
|--------|------------------------------:|-----------------:|---------------:|------------:|------------:|
| Sniper·TwoAgree·ADX·max2 (v1.1 default) | 0.21 | 1.14 | 2% | 0.24 | 0.24 |
| Sniper·TwoAgree·noADX·max3 | 0.30 | 1.22 | 4% | 0.36 | 0.30 |
| Sniper·Any·ADX·max3 | 1.06 | 1.65 | 29% | 1.08 | 1.14 |
| Sniper·Any·noADX·max3 | 1.40 | 1.82 | 43% | 1.49 | 1.49 |
| Scanner·TwoAgree·ADX·max3 | 0.54 | 1.26 | 9% | 0.53 | 0.61 |
| Scanner·Any·noADX·max3  ★ target≥2/day | 1.90 | 2.20 | 64% | 2.10 | 1.93 |
| Scanner·Any·noADX·max4 | 2.09 | 2.42 | 64% | 2.31 | 2.17 |
| Scanner·Any·noMute·max4 | 2.33 | 2.64 | 68% | 2.46 | 2.49 |

**Best for frequency:** `Scanner·Any·noADX·max3  ★ target≥2/day`

### Practical reading

- **v1.1 default (Sniper · Two agree · ADX · max2)** stays near **~1 entry on a signal day**, and many days are flat — that is by design.
- To push toward **≥2 entries/day**, use **Scanner + Any engine**, raise **Max chart entries/day to 3–4**, and consider turning **ADX off** (and optionally midday mute).
- More entries ≠ better PnL. Prior SL18 lab: looser gates cut expectancy. Trade the frequency setting small.

## By strike (recommended frequency config)

Config: **Scanner·Any·noADX·max3  ★ target≥2/day**

| Side | Strike | Moneyness | Trades | /session-day | /active-day | % days ≥2 | T1% | Net |
|------|-------:|-----------|-------:|-------------:|------------:|----------:|----:|----:|
| CE | 24200 | ITM | 124 | 2.10 | 2.34 | 73% | 71% | 219.3 |
| CE | 24250 | ITM | 122 | 2.07 | 2.30 | 73% | 70% | 184.5 |
| CE | 24300 | ATM | 124 | 2.10 | 2.30 | 73% | 70% | 219.3 |
| CE | 24350 | OTM | 112 | 1.90 | 2.11 | 64% | 70% | 167.8 |
| CE | 24400 | OTM | 95 | 1.61 | 1.94 | 51% | 70% | 200.6 |
| PE | 24200 | OTM | 93 | 1.58 | 1.94 | 51% | 66% | 24.3 |
| PE | 24250 | OTM | 107 | 1.81 | 2.18 | 63% | 66% | 102.8 |
| PE | 24300 | ATM | 114 | 1.93 | 2.28 | 66% | 69% | 164.2 |
| PE | 24350 | ITM | 115 | 1.95 | 2.30 | 64% | 67% | 75.0 |
| PE | 24400 | ITM | 115 | 1.95 | 2.35 | 64% | 65% | 38.2 |

Files: `STRIKE_RATE_FREQ_SUMMARY.csv`, `STRIKE_RATE_FREQ_BY_STRIKE.csv`, `backtest_strike_rate_frequency.py`