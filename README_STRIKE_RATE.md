# STRIKE RATE — Indian index options signal engine

Production-style indicator for **Nifty / Bank Nifty / Sensex CE & PE** charts.  
Engines read the **index/futures feed**; you trade the **option premium**.

See **`STRIKE_RATE_AUDIT.md`** for the full right/wrong/improve review.

## Recommended setup (v1.1)

| Setting | Value |
|---------|--------|
| Mode | **Sniper** |
| Chart signals | **Two must agree** (same-bar votes) |
| Signal TF | **5** |
| Target 1 | **10** (book half · stop → entry) |
| Target 2 | **30** (runner half) |
| Stop | **18** |
| Hold to T1 | **ON** |
| ADX chop filter | **ON** (min 18) |
| Max chart entries / day | **2** |

## v1.1 accuracy fixes

- Confluence requires **N engines firing entry on the same bar** (not “already in from earlier”).
- **Hold to T1** blocks engine signal-exits until half is banked (SL / T2 / EOD still work).
- Dashboard **T1% = booked**, not MFE touch on a stop bar.
- Optional **ADX** + **max entries/day**.

## Lab findings baked into defaults

From this repo’s Nifty multi-strike work (`BACKTEST_SL18_REPORT.md`):

- **SL 18** — tighter stops (10–15) sat inside premium noise and cut winners.
- **Runner required** — full exit at +10 with SL18 was net-negative; half@T1 / half@T2 is the plan.
- **Strict confluence** — fewer, cleaner entries (~1 signal class / ATM chart / day).
- Broad panel was harsher than marketing “54% T1 / 7% SL” claims: treat dashboard stats as **your chart only**.
- **+10 every day is not a design target** — expectancy is per-expiry with runners.

## OI walls (daily support / resistance)

TradingView Pine cannot HTTP-fetch NSE. Use **`fetch_oi_walls.py`** to bake Support (max Put OI) / Resistance (max Call OI) into the script, or try the TV ladder fallback.

## Quick start

1. Open an **ATM** option chart (5m view is fine; signals stay on 5m).
2. Paste `Strike_Rate.pine`.
3. Set **Index feed** → `NSE:NIFTY1!` (or BankNifty / Sensex futures).
4. Leave v1.1 defaults. Green = in trade · pale green = T1 banked · red = flat.

## Files

- `Strike_Rate.pine` — main indicator (v1.1)
- `STRIKE_RATE_AUDIT.md` — full audit
- `BACKTEST_SL18_REPORT.md` — SL=18 lab tables
- `Nifty_Options_Confluence.pine` — earlier confluence lab (reference)
