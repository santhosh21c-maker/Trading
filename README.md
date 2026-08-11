# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of PxTrading **Decider / Target** ladder.

## Extend behaviour (locked)

| Segment | Changing **Extend** does |
|---------|---------------------------|
| **Robot Prediction** | Changes **Decider / Target price levels** (LIVE). Does **not** lengthen lines. |
| **INDIAN** | Levels **fixed** for the day. Extend **only** lengthens lines. |

## Ladder (exact on vendor numbers)

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## Vendor Robot PUT 24500 (same clock time ≈11:00, price ≈61.70)

| Extend | Decider | H / L / C / B |
|--------|---------|----------------|
| 50 | 72.22 / 71.59 | 77.15 / 66.65 / 71.91 / 5.25 |
| 60 | 65.97 / 65.48 | 69.75 / 61.70 / 65.73 / 4.03 |

**H50 > H60 at one time** ⇒ nested last/first-N is impossible. Default window = **Auto lag**:

```text
lag = max(0, 5 * (60 - Extend))
Ext50 → lag 50 → bars [50..99]  (older morning, before deep dump)
Ext60 → lag  0 → bars [1..60]   (recent)
```

Trim extremes default **10%** (lifts Ext60 L off crash bars).

## Test protocol (same replay time)

1. Paste script, reset inputs, Robot Window = Auto lag.
2. Replay PUT 24500 to **~11:00** (price near 61–62).
3. Ext **50** → chip should near H77.15 L66.65 / Dec 72.22/71.59.
4. Ext **60** → chip should near H69.75 L61.70 / Dec 65.97/65.48.
5. Send both chips (`alag n=… lag=… HHMM-HHMM`).
