# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of PxTrading **Decider / Target** ladder.

## Extend behaviour (locked)

| Segment | Changing **Extend** does |
|---------|---------------------------|
| **Robot Prediction** | Changes **Decider / Target price levels** (lookback). Does **not** lengthen lines. |
| **INDIAN** | Levels **fixed** for the day. Extend **only** lengthens lines. |

## Ladder (exact on vendor numbers)

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## Vendor Robot PUT 24500

| Extend | Decider | H / L / C / B |
|--------|---------|----------------|
| 50 | 72.22 / 71.59 | 77.15 / 66.65 / 71.91 / 5.25 |
| 60 | 65.97 / 65.48 | 69.75 / 61.70 / 65.73 / 4.03 |

H50 > H60 ⇒ window is **not** nested last-N. Default Robot window = **Shifted [Ext, 2Ext)**.

## Test

1. Robot Ext **50** → note Decider + chip H/L  
2. Ext **60** → Decider **must change**; line length should look the same (`extend.right`)  
3. Indian → change Ext → Decider unchanged; lines longer/shorter  
4. Send chip H/L/C/B/Dec for Ext 50 and 60 on PUT 24500  
