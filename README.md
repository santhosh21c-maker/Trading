# Options Buy Decider & Targets

Practical Pine indicator for **options BUYING** on **NIFTY / BANKNIFTY / SENSEX** option charts (**1m & 5m**).

Use on the **option premium chart** (CE or PE) for **any strike** — levels and signals scale to that chart’s price.

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

## Entry rules (upside & downside)

Valid both ways on the strike you are viewing:

1. **Decider → Target 1 (fixed)**  
   After price visits the Decider zone, enter toward Target 1. Target for this leg is **T1**.

2. **If Target 1 is broken** (close beyond T1)  
   Expect the move to continue to **Target 4** (`EXTEND` signal). Stop can trail to Decider.

3. **Reversal if Target 4 fails**  
   If price touches T4 for N bars without a close break → **REV** from T4 back toward **Target 1 / Decider**.

| Signal | Meaning |
|--------|---------|
| `BUY T1` | Upside Decider → T1 |
| `DN T1` | Downside Decider → T1 |
| `EXTEND` | T1 broken → hold/add for T4 |
| `REV DN` / `REV UP` | T4 failed → reverse to T1/Decider |
| `STOP` / `TARGET` | Exit markers |

## Stop (adjustable)

Settings → **Stop — adjustable**:

- **Beyond Decider × B** — stop past Decider by `Stop size × B` (default)
- **Fixed Points** — absolute premium points
- **ATR ×** — `Stop size × ATR`

Optional: trail stop to Decider after T1 break.

## Defaults (IST)

- Session start `09:15`, skip `5` min → OR window **09:20–09:50** (30 min)
- Tune OR length / skip for your style
- Prediction lookback default `50` bars

## Files

- `Options_Buy_Decider_Targets.pine` — **use this** (paste into TradingView)
- `Smart_Robotic_Logic_Decider_Targets.pine` — earlier vendor reverse-engineer (abandoned)

## Not financial advice

Educational tool for structure and planning. Always manage risk; options can go to zero.
