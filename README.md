# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of PxTrading **Decider / Target** ladder.

## Extend behaviour (locked)

| Segment | Changing **Extend** does |
|---------|---------------------------|
| **Robot Prediction** | Changes **Decider / Target price levels** (LIVE lookback). Does **not** lengthen lines. |
| **INDIAN** | Levels **fixed** for the day. Extend **only** lengthens lines. |

## Ladder (exact on vendor numbers)

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## Vendor Robot PUT 24500 — important

| Extend | Decider | H / L / C / B | Replay time to test |
|--------|---------|----------------|---------------------|
| 50 | 72.22 / 71.59 | 77.15 / 66.65 / 71.91 / 5.25 | **~10:10–10:20** |
| 60 | 65.97 / 65.48 | 69.75 / 61.70 / 65.73 / 4.03 | **~11:30–11:40** |

Vendor Ext50 has **H=77** but Ext60 has **H≈70**. At one clock time, nested first/last-N windows **cannot** produce H50 > H60 (longer window always keeps the higher high). Those two vendor chips are almost certainly from **different replay times**: early (77 still in last-50, dump not yet in window) vs later (77 aged out, bounce range).

Default Robot window = **Last Ext bars** (LIVE rolling lookback) + Body low.

## Test protocol

1. Paste script, Segment = Robot Prediction, Window = Last Ext bars, reset inputs.
2. Replay PUT 24500 to **~10:15**, set Extend **50** → Decider should near **72.22 / 71.59** (chip H~77, L~66).
3. Continue replay to **~11:35**, set Extend **60** → Decider should near **65.97 / 65.48** (chip H~70, L~62).
4. Indian → change Ext → Decider unchanged; lines longer/shorter.
5. Send both chips (include the `HHMM-HHMM` window span).
