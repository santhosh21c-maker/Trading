# Online OI → Support / Resistance

## Short answer

**Pine Script cannot download OI from the internet.**  
TradingView indicators are sandboxed — no NSE / Sensibull HTTP calls from the chart.

**What we can do:** fetch live NSE option-chain OI **outside** TradingView, then bake Support / Resistance into `Strike_Rate.pine`.

## Bridge already in this repo

```bash
python3 fetch_oi_walls.py          # NIFTY nearest expiry
python3 fetch_oi_walls.py BANKNIFTY
```

That script:
1. Pulls the live NSE index option chain (`jugaad_data`)
2. Sets **Support** = strike with max **Put OI**
3. Sets **Resistance** = strike with max **Call OI** (next distinct CE wall if both pin ATM)
4. Writes `oi_walls.json` and updates the `ONLINE_OI_*` block inside `Strike_Rate.pine`

Then re-paste / refresh the indicator on TradingView (raw GitHub URL or copy-paste).

## In the indicator

Settings → **⑤ OI walls** → source **Online NSE (baked)** (default).

- **Index / futures chart** (price > 1000): draws S/R **lines** at those strikes  
- **Option premium chart**: shows strikes in the **live panel + labels** (y-axis is premium, not index)

## Today’s bake (example — re-run to refresh)

See `oi_walls.json` for the latest fetch timestamp, spot, expiry, and top OI strikes.
