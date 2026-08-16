# Nifty Options Confluence v1.1 — TP1 lock (+10 minimum)

## What changed (your request)

You asked to fine-tune so **every trade captures at least +10** (CE or PE).

**Hard truth:** with any stop-loss, **100% of trades cannot be guaranteed +10** — if premium never reaches entry+10 and hits SL first, that trade loses. Removing SL would “force” +10-or-hold but allows unlimited loss.

**What we did instead:** maximize **TP1-first** rate and **book full size at +10**.

## v1.1 defaults (from search)

| Setting | Value | Why |
|---------|--------|-----|
| **TP1 lock mode** | ON | Exit **full** at TP1 → banks **+10** when hit |
| **Hold to TP1** | ON | No confluence SELL before +10 |
| **TP1** | **10** | Your minimum capture |
| **SL** | **30** | Wider stop so +10 usually prints first |
| **Min BUY score** | **5** | Fewer / cleaner entries |
| **Require E7** | ON | ATR impulse — biggest filter lift |
| **Require E3** | ON | VWAP reclaim gate |
| Max entries / day | 3 | Avoid overtrading |

## Search result (multi-strike sample)

With score **5** + require **E7** + SL **30** + hold/exit at TP1:

| Metric | Value |
|--------|------:|
| Trades | 12 |
| Hit +10 before SL | **11 / 12 → ~91.7%** |
| Net pts (sample) | **+80** |
| Avg pts / trade | **+6.67** |

Tighter SL (10–15) **destroys** the +10-first rate on the same entries. That is why losses were still appearing with SL=10.

## How to use

1. Open your **Nifty CE or PE** chart (3m / 5m).
2. Paste `Nifty_Options_Confluence.pine` (v1.1).
3. Leave **TP1 lock mode** ON.
4. Expect: **BUY → hold → SELL at TP1 +10**, or rare **SL −30**.
5. Optional runners: turn **TP1 lock mode OFF**, enable BE/trail after TP1.

## Files

- `Nifty_Options_Confluence.pine` — indicator v1.1
- `tp1_lock_search.csv` / `tp1_lock_best.json` — grid that produced these defaults
- `BACKTEST_MULTISTRIKE_NIFTY.md` — earlier v1.0 multi-strike report (SL=10, more SL hits)
