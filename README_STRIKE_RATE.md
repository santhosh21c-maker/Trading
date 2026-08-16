# STRIKE RATE — Indian index options signal engine

Production-style indicator for **Nifty / Bank Nifty / Sensex CE & PE** charts.  
Engines read the **index/futures feed**; you trade the **option premium**.

## Recommended setup

| Setting | Value |
|---------|--------|
| Mode | **Sniper** |
| Chart signals | **Two must agree** |
| Signal TF | **5** |
| Target 1 | **10** (book half · stop → entry) |
| Target 2 | **30** (runner half) |
| Stop | **18** |

## Lab findings baked into defaults

From this repo’s Nifty multi-strike work (`BACKTEST_SL18_REPORT.md`):

- **SL 18** — tighter stops (10–15) sat inside premium noise and cut winners.
- **Runner required** — full exit at +10 with SL18 was net-negative; half@T1 / half@T2 is the plan.
- **Strict confluence** — fewer, cleaner entries (~1 signal class / ATM chart / day).
- Broad panel was harsher than a cherry-picked pocket: treat dashboard stats as **your chart only**, and size small until your log agrees.

## Quick start

1. Open an **ATM** option chart (5m view is fine; signals stay on 5m).
2. Paste `Strike_Rate.pine`.
3. Set **Index feed** → `NSE:NIFTY1!` (or BankNifty / Sensex futures).
4. Leave defaults. Green = in trade · pale green = T1 banked · red = flat.

## Files

- `Strike_Rate.pine` — main indicator
- `BACKTEST_SL18_REPORT.md` — SL=18 lab tables
- `Nifty_Options_Confluence.pine` — earlier confluence lab (reference)
