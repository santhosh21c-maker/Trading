# STRIKE RATE — Full Audit

**Scope:** Code logic, trade plan, and fitness for “≥10 option points / day on CE & PE.”  
**Sources:** `Strike_Rate.pine` (repo), your pasted script, `BACKTEST_SL18_REPORT.md` (128-runner lab).

---

## Verdict

Strike Rate is a **solid signal + trade-plan shell** for ATM option charts (index engines → premium trade). It is **not** a system that can deliver +10 points every day, or on every trade, while keeping a finite stop.

| Claim | Reality |
|-------|---------|
| Header “772 trades · 54% T1 · 7% stop” (some pasted copies) | **Not verified** in this repo. Lab panel: **~38% T1 · ~63% SL** @ SL18 runners. |
| Recommended plan T1 10 / T2 30 / SL 18 · half@T1 | **Correct design** vs full lock-at-10 (deeply red in lab). |
| Sniper · Two must agree · 5m | **Right frequency class** (~1 signal / ATM chart / day when gates are strict). |
| Goal: +10 every day CE+PE | **Incompatible** with ~1 signal/day and ~⅓–½ T1 reach. |

---

## What is right

1. **Option chart + index engines** — Direction from futures/`request.security`; PnL in option points. Correct product shape.
2. **Trade plan math** — Half at +10, stop → entry, runner to +30. Lab showed full exit at +10 with SL18 ≈ −7.5 pts/trade; runners required.
3. **SL 18** — Tighter stops (10–15) sat inside premium noise. Gap budget ~1.3× is correctly warned.
4. **Session / midday mute / EOD flat** — Sensible for Indian cash session.
5. **CE/PE sync via correlation** — Blocks trading a call while premium moves against the index.
6. **Early warning excluded from stats** — Honest.
7. **Dashboard disclaimer** — No slippage / brokerage (keep believing that).

---

## What is wrong or misleading

### 1. Confluence counts “engines already in,” not “engines agreeing now” (logic bug)

```pine
// index 8 — Two must agree
ac = count of stIn[j] for enabled engines
ent[8] = ac >= consN
```

Effects:

- Chart BUY can fire because **two engines entered on different bars** (lag / second-wave), not because two fired together.
- Default chart track is this row — so labels/alerts inherit the quirk.
- **Fix (v1.1):** vote on **fresh entry flags** the same bar (`ent[j]`), require `votes >= 2`.

### 2. Signal exits can cut before T1

Each engine has its own `exi` (cross back VWAP, SuperTrend flip, etc.). Those exits run **before** T1 unless blocked. Lab confluence preferred **hold-to-TP1**.

**Fix (v1.1):** `Hold to T1` default ON — ignore signal exits until half is banked (SL / T2 / EOD still apply).

### 3. Dashboard “T1%” is MFE, not booked

`nHit` increments when `max(high − entry) >= tp1`. Same-bar **SL + spike to T1** can inflate Hit% without ever booking half.

**Fix (v1.1):** T1% = trades that **actually set `st1`** (booked). Keep MFE in “Best”.

### 4. Header stats conflict with lab

| Metric | Pasted marketing header | Repo lab (`BACKTEST_SL18`) |
|--------|-------------------------|----------------------------|
| Trades | 772 (unverified) | 128 runners / 40 contracts |
| Reach T1 | ~54% | ~38% |
| Stop out | ~7% | ~63% |
| Net | implied strong | All-strike −185; ATM ~flat/+14 |

Trust the **lab panel** and **your chart dashboard**, not the 772-trade blurb.

### 5. “+10 points every trade / every day”

With SL = 18 and ~38–54% T1:

- Expectancy is carried by **runners**, not by locking +10.
- Many sessions: **zero** signals (ATM ~0.13 calls/session-day in lab).
- Guaranteeing +10 with a stop is **impossible** — wrong days exist.

### 6. Smaller issues

| Item | Note |
|------|------|
| `premOK = close > close[1]` | Weak filter; green bar ≠ impulse. |
| Daily pivots `lookahead_on` + `[1]` | Standard prior-day pattern; OK on confirmed bars. |
| Signal TF 1 / 3 | Untested vs 5m lab. |
| OI walls | Baked NSE via `fetch_oi_walls.py` — must refresh; not live inside TV. |
| BankNifty / Sensex defaults | Same 10/30/18 — raise proportionally. |
| Correlation window 20 | Can fail on thin/new contracts. |

---

## Accuracy: how to improve (priority order)

| Priority | Change | Why |
|----------|--------|-----|
| P0 | Vote-based confluence | Stops lag / second-wave BUYs |
| P0 | Hold to T1 (default on) | Stops engine exits from eating winners |
| P0 | Booked T1% on dashboard | Honest hit rate |
| P1 | ADX chop filter on index | Skip dead midday-style grind outside mute |
| P1 | Max 1–2 entries / day | Matches lab frequency; avoids revenge stacking |
| P2 | Stronger premium confirm (body / ATR) | Replaces bare `premOK` |
| P2 | Refresh OI walls daily | Context only — not an entry trigger alone |
| P2 | Size for 1.3× stop | Risk model, not signal |

What will **not** magically raise accuracy: more engines (Scanner), “Any engine”, locking full at +10, or claiming institutional prediction.

---

## Recommended live recipe (unchanged economics, fixed mechanics)

1. ATM CE **or** PE from your bias · 5m signals · view 1m/3m OK  
2. Mode **Sniper** · Chart **Two must agree** (v1.1 votes)  
3. T1 **10** · T2 **30** · Stop **18** · Hold to T1 **ON**  
4. One contract small until **your** dashboard Total > 0 for a full expiry  
5. Expect: most days flat; signal days ~1 entry; size so −18×1.3 is acceptable  

---

## Files

| File | Role |
|------|------|
| `Strike_Rate.pine` | Indicator (**v1.1** = audit fixes) |
| `STRIKE_RATE_AUDIT.md` | This document |
| `BACKTEST_SL18_REPORT.md` | Lab numbers behind SL18 / runners |
| `README_STRIKE_RATE.md` | Quick start |
| `fetch_oi_walls.py` | Refresh baked OI S/R |

---

## Bottom line

**Keep** the product shape and the 10 / 30 / 18 half-runner plan.  
**Fix** confluence voting, hold-to-T1, and dashboard honesty (done in v1.1).  
**Drop** any expectation of +10 every day — chase **positive expectancy per expiry**, not a daily guarantee.
