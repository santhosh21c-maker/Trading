# Option chart level crack

Corrected logic for pre-open purple/green/black/red horizontals on Nifty option TBT charts.

- **`OPTION_CHART_LINES_CRACK.md`** — green = prior close, red = CPR BC `(H+L)/2`, optional red₂ = `C+(H−L)`; purples unresolved
- **`Option_PreOpen_CPR.pine`** — plots those levels from the option’s previous Daily candle
- **`verify_option_chart_levels.py`** — re-fetch NSE FO OHLC and reprint the proof table
