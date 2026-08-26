# STRIKE RATE — How to use

## Presets

| Preset | Settings | Entries / day (lab) |
|--------|----------|---------------------|
| **Frequency (≥2/day)** ← default | Scanner · Any engine · max 3 · ADX off | ATM CE **~2.1** · ATM PE **~1.9** · ≥2 on ~70% of days |
| **Quality (Sniper)** | Sniper · Two must agree · max 2 · ADX on | ~**0.3**/session-day · ~1.2 on active days |

Source: `STRIKE_RATE_FREQ_REPORT.md` (59 Nifty sessions, ATM±100 CE/PE).

Trade plan (both presets): **T1 10 / T2 30 / Stop 18** · half@T1 · Hold to T1 ON.

## Quick start

1. ATM option chart · paste `Strike_Rate.pine`
2. Index feed → `NSE:NIFTY1!`
3. Leave **Preset = Frequency (≥2/day)** if you want ~2 entries/day
4. Switch to **Quality** if you prefer fewer, stricter signals

## OI walls

Context only (not entries). Refresh with `fetch_oi_walls.py` for baked NSE S/R.

## Files

- `Strike_Rate.pine` — indicator
- `STRIKE_RATE_FREQ_REPORT.md` — entries/day by config & strike
- `STRIKE_RATE_AUDIT.md` — logic audit
- `BACKTEST_SL18_REPORT.md` — SL18 expectancy lab
