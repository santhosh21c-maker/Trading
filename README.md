# Options Buy Decider & Targets

Pine indicator for **NIFTY / BANKNIFTY / SENSEX** option charts (**1m & 5m**).

Draws **Decider** and **Target 1–4** as clear support / resistance lines on the **option premium** chart for any strike you open. No buy/sell signals.

## Modes

| Mode | Behaviour |
|------|-----------|
| **INTRADAY** | Opening Range builds after open, then **freezes** — levels stay fixed for the day. |
| **PREDICTION** | Live rolling lookback — levels update as the window moves. |

## Ladder

```text
C = (H + L) / 2
B = max((H - L) / 2, ATR floor)
Decider  = C +/- 0.06*B
Target N = C +/- {1.00, 1.54, 1.83, 2.08}*B
```

## Levels on chart

- Decider High / Decider Low
- Target 1–4 High / Low

Lines plot through the session with labels. Use as S/R on the strike you are viewing.

## Defaults IST

- Session start `09:15`, skip `5` min → OR **09:20–09:50**

## Files

- `Options_Buy_Decider_Targets.pine` — use this
- `Smart_Robotic_Logic_Decider_Targets.pine` — older reference only

Educational only — not financial advice.
