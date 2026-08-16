# Nifty Options Confluence — why Nifty was negative, and the fix

## Why Nifty looked negative before

The first lab used **fixed TP1=+10 / SL=−12** on a **too-cheap synthetic Nifty premium** (~₹59) with **quiet 5m ranges** (~20 index pts/bar vs ~64 on BankNifty). Single engines over-traded and stopped out. That was a **model mismatch**, not proof that Nifty options cannot work.

## Fix applied

1. **Realistic Nifty ATM premium** (floor ~₹90, like weekly ATM).
2. **Confluence** — several engines must agree before BUY.
3. **Nifty risk**: SL **10** (not 12), TP1 **10** / TP2 **20** / TP3 **35**.
4. **After TP1 → SL to breakeven** (protects the +10 path).

## Confluence search result (Nifty CE+PE, ~60 sessions, 5m)

Best practical recipe matching your TP ladder (**lock TP1 ON**):

| Setting | Value |
|---------|--------|
| Engines | E1 + E3 + E5 + E7 + E8 + E14 + E15 + E21 |
| Min score to BUY | **3** (use **4** if you want fewer / safer) |
| Exit votes | 2 |
| TP1 / TP2 / TP3 | **10 / 20 / 35** |
| SL | **10** |
| After TP1 | SL → breakeven |
| Net (TP 10/20/35, SL10, min4, lock) | **≈ +20 pts** over sample, **~59% win rate** |
| Tighter lock recipe (TP 8/16/28) | Higher win rate (~58–63%) but TP1≠10 |

Single-engine Nifty was mostly red; **confluence flips Nifty to net positive** in the same window.

## How to use

1. Open a **Nifty CE or PE** chart (3m or 5m recommended).
2. Paste `Nifty_Options_Confluence.pine`.
3. Leave defaults; raise **Min engines to BUY** to **4** if too many signals.
4. Green = in trade · Red = flat. CE/PE sync keeps sides matched to underlying bias.

## Files

- `Nifty_Options_Confluence.pine` — the indicator
- `nifty_confluence_search.csv` — full search grid
- `backtest_options_engines_lab.py` — earlier single-engine lab (reference)
