# Options Buy Decider & Targets

Practical Pine indicator for **options BUYING** on **NIFTY / BANKNIFTY / SENSEX** option charts (**1m & 5m**).

Use on the **option premium chart** (CE or PE), not the index.

## Modes

| Mode | Behaviour |
|------|-----------|
| **INTRADAY** | Opening Range builds after open (skip noise), then **freezes** for the day — stable Decider/Targets. |
| **PREDICTION** | Live rolling Donchian lookback — levels adapt as the session unfolds. |

## Ladder

```text
C = (H + L) / 2
B = max((H - L) / 2, ATR × floor)   // ATR floor keeps levels meaningful
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## How to trade (BUY only)

On the option chart, premium **up** = your long works.

1. Wait for **INTRADAY** status `FROZEN` (OR complete), or use **PREDICTION** live.
2. **BUY** when price breaks **above Decider High** (green label).
3. Scale / exit at **Upper Target 1–4**.
4. **EXIT / protect** if price falls back **under Decider Low**, or after Target 1 tag.

Alerts are included for BUY and EXIT.

## Defaults (IST)

- Session start `09:15`, skip `5` min → OR window **09:20–09:50** (30 min)
- Tune OR length / skip for your style
- Prediction lookback default `50` bars

## Files

- `Options_Buy_Decider_Targets.pine` — **use this**
- `Smart_Robotic_Logic_Decider_Targets.pine` — earlier vendor reverse-engineer (abandoned)

## Not financial advice

Educational tool for structure and planning. Always manage risk; options can go to zero.
