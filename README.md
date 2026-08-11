# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of PxTrading **Decider / Target** ladder.

## Ladder (verified)

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## Robot Auto window (current)

| Extend | Window | Why |
|--------|--------|-----|
| **&lt; 60** (e.g. 50) | **Opening range** = first Ext bars after 09:15 | Keeps morning H~77; ends ~10:04 before dump |
| **≥ 60** | **Last Ext bars** + trim lows 15% | Recent range; Ext60 chip already Dec 65.10 vs aim 65.97 |

Vendor Ext50 H&gt;Ext60 H at one time ⇒ cannot be nested last-N for both.

## Vendor aims (PUT 24500)

| Ext | Decider | H / L |
|-----|---------|-------|
| 50 | 72.22 / 71.59 | 77.15 / 66.65 |
| 60 | 65.97 / 65.48 | 69.75 / 61.70 |

## Test (same replay ~11:00–11:10)

1. Reset inputs. Window = Auto (OR if Ext&lt;60 / Last if Ext≥60).
2. Ext **50** → chip `or n=50 915-1004` (approx) → aim Dec 72.22.
3. Ext **60** → chip `last n=60 …` → aim Dec 65.97.
4. Send both chips.
