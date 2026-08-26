# STRIKE RATE — How to use

## Presets

| Preset | Settings | Entries / day (lab) |
|--------|----------|---------------------|
| **Frequency (≥2/day)** ← default | Scanner · Any engine · max 3 · ADX off | ATM CE **~2.1** · ATM PE **~1.9** · ≥2 on ~70% of days |
| **Quality (Sniper)** | Sniper · Two must agree · max 2 · ADX on | ~**0.3**/session-day · ~1.2 on active days |

Source: `STRIKE_RATE_FREQ_REPORT.md` (59 Nifty sessions, ATM±100 CE/PE).

Trade plan (both): **T1 10 / T2 30 / Stop 18** · half@T1 · Hold to T1 ON.

## Option-buyer filters (v1.2 — default ON)

| Filter | Default | What it does |
|--------|---------|----------------|
| **DTE gate** | Min DTE **3** | No new buys when days-to-expiry ≤ 3. Set **Manual expiry YYMMDD** if the ticker parse fails. |
| **IV regime** | Max IV rank **70%** | Uses **India VIX** 60-day rank; blocks when vol is already rich. |
| **Post-SL cooldown** | **30 min** | After a chart-track stop, no new chart entry until cooldown ends. |

Live panel shows **DTE / IV rank / Cooldown** (green = ok, red/amber = blocking).

## Quick start

1. ATM option chart · paste `Strike_Rate.pine`
2. Index feed → `NSE:NIFTY1!`
3. Confirm **Manual expiry YYMMDD** matches your contract (or rely on Auto)
4. Leave **Preset = Frequency (≥2/day)** for ~2 entries/day
5. Use **Quality** if you want fewer, stricter signals

## OI walls

Context only (not entries). Refresh with `fetch_oi_walls.py` for baked NSE S/R.

## Files

- `Strike_Rate.pine` — indicator (v1.2)
- `STRIKE_RATE_FREQ_REPORT.md` — entries/day by config & strike
- `STRIKE_RATE_AUDIT.md` — logic audit
- `BACKTEST_SL18_REPORT.md` — SL18 expectancy lab
