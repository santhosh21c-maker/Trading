# SL=18 Backtest Report — Nifty Options Confluence v1.1

**Config:** SL **18** · TP **10 / 20 / 35** · min score **5** · require **E7 + E3** · hold to TP1  
**Data:** 4 monthly expiries (Apr–Jul 2025) · **40 contracts** (5 CE + 5 PE around ATM each) · 1h paths IV-calibrated to **real NSE daily** option OHLC  
**Note:** Not live 5m ticks. Apr produced almost no post-warmup signals under score-5 gates.

---

## Calls per day (what you’ll feel live)

| Lens | Result |
|------|--------|
| On a day you **do** get a signal | **~1.2 entries** (median **1**, max **2** with `maxDay=3`) |
| ATM CE **or** PE alone, all session days | **~0.13 calls/day** (~1 entry every **7–8** sessions) |
| ATM CE+PE combined | **~0.26 calls/day**; **~19%** of days have ≥1 signal |

Strict gates keep frequency low on purpose.

---

## Headline — RUNNERS (hold to TP1 → BE → trail → TP3)

This is the mode that can print TP1 / TP2 / TP3.

| Metric | All 40 contracts | ATM only |
|--------|----------------:|---------:|
| Trades | **128** | **27** |
| Reached **TP1** | **48 (37.5%)** | **10 (37%)** |
| Reached **TP2** | **41 (32.0%)** | **10 (37%)** |
| Reached **TP3** | **35 (27.3%)** | **9 (33%)** |
| Exit **SL** | **80 (62.5%)** | **17 (63%)** |
| Exit BE/trail | 13 | — |
| Exit TP3 | 35 | 9 |
| Net pts | **−185** | **+14** |
| Avg / trade | −1.45 | +0.52 |
| Win rate | 32% | — |

### By side (all strikes)

| Side | Trades | TP1 | TP2 | TP3 | SL | Net |
|------|-------:|----:|----:|----:|---:|----:|
| CE | 34 | 7 | 7 | 7 | 27 | **−241** |
| PE | 94 | 41 | 34 | 28 | 53 | **+56** |

### By expiry (runners)

| Expiry | Trades | TP1 | TP2 | TP3 | SL | Net | Calls/active day |
|--------|-------:|----:|----:|----:|---:|----:|-----------------:|
| 2025-05-29 | 62 | 25 | 20 | 14 | 37 | −146 | 1.09 |
| 2025-06-26 | 48 | 10 | 8 | 8 | 38 | −404 | 1.20 |
| 2025-07-31 | 18 | 13 | 13 | 13 | 5 | **+365** | 1.38 |

Jul PE trend carried the sample; Jun was the painful month.

---

## Headline — TP1 LOCK (exit full at +10)

| Metric | Value |
|--------|------:|
| Trades | 130 |
| Hit TP1 / exit +10 | **49 (37.7%)** |
| TP2 / TP3 | 0 (exits at TP1) |
| SL | **81 (62.3%)** |
| Net | **−968** |
| Avg | −7.45 |

With **SL=18**, locking at +10 is **not enough** — too many −18s vs +10s. Runners (letting winners reach TP2/TP3) are required for SL=18 to have a chance.

---

## Variant sweep (ATM ±50 only, 24 contracts, 1h)

| Variant | Mode | Trades | TP1 | TP2 | TP3 | SL | Net | Avg | ATM calls/day |
|---------|------|-------:|----:|----:|----:|---:|----:|----:|--------------:|
| score5+E7+E3 | runners | 80 | 33 | 31 | 28 | 47 | **+149** | +1.86 | 0.14 |
| score5+E7+E3 | lock | 81 | 34 | 0 | 0 | 47 | −506 | −6.25 | 0.14 |
| score4+E7 | runners | 207 | 70 | 55 | 44 | 137 | −871 | −4.21 | 0.33 |
| score3+E7 | runners | 214 | 74 | 59 | 48 | 140 | −785 | −3.67 | 0.35 |
| score3 no gates | runners | 303 | 119 | 99 | 77 | 184 | −507 | −1.67 | 0.49 |

**Tightest entry (v1.1) + runners** was the only net-positive cell in this sweep.

---

## Practical takeaway for SL=18

1. Expect **~1 call on a signal day**, not many per day.
2. Roughly **~1 in 3** trades tag TP1; most of those that clear TP1 also reach TP2/TP3 on this sample.
3. **~2 in 3** still stop out at −18 under these paths.
4. Prefer **runners** (not full exit at TP1) when SL=18.
5. Prefer **ATM / mild OTM PE** in down months; CE struggled in this window.
6. Earlier **~75% TP1-first @ SL18** was a **small 12-trade** pocket — the **128-trade** panel is closer to **~38%**.

---

## Files

- `BACKTEST_SL18_RUNNERS_TRADES.csv` / `BACKTEST_SL18_RUNNERS_SUMMARY.csv`
- `BACKTEST_SL18_LOCK_TRADES.csv` / `BACKTEST_SL18_LOCK_SUMMARY.csv`
- `BACKTEST_SL18_VARIANTS.csv`
- `BACKTEST_SL18_META.json`
- `Nifty_Options_Confluence.pine` — default **SL=18**
