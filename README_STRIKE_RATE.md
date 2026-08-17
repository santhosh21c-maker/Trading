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

## OI walls (daily support / resistance)

**Partially automatic.** TradingView does not expose a full NSE option-chain API to Pine.

What Strike Rate does:
1. You set **Expiry YYMMDD** (update when it rolls).
2. Script takes ATM from the index feed and builds ±N strikes.
3. Pulls **open interest** on each CE/PE (daily). If OI is blank on TV, it falls back to **volume** as a wall proxy.
4. **Max Put wall → Support** · **Max Call wall → Resistance**
5. Shown in the live panel + optional chart labels.

Limits:
- These are **index strikes**, not premium price lines (option chart y-axis is premium).
- Symbol format can differ — switch **Symbol format** in settings if walls stay “No data”.
- Not a substitute for Sensibull / NSE chain for full OI analytics.

## Quick start

1. Open an **ATM** option chart (5m view is fine; signals stay on 5m).
2. Paste `Strike_Rate.pine`.
3. Set **Index feed** → `NSE:NIFTY1!` (or BankNifty / Sensex futures).
4. Under **⑤ OI walls**, set **Expiry YYMMDD** for the contract you trade.
5. Leave other defaults. Green = in trade · pale green = T1 banked · red = flat.

## Files

- `Strike_Rate.pine` — main indicator
- `BACKTEST_SL18_REPORT.md` — SL=18 lab tables
- `Nifty_Options_Confluence.pine` — earlier confluence lab (reference)
