# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of the PxTrading-style **Decider / Target** ladder.

## Segment behaviour (locked)

| Segment | What **Extend** does |
|---------|----------------------|
| **Robot Prediction** | Changes **Decider / Targets** (prediction lookback) **and** draws lines further right |
| **INDIAN** | Levels **fixed for the day** (prior-day H/L). Extend **only** lengthens lines |

## Ladder

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## Vendor Robot reference (PUT 24500)

| Extend | Decider | H / L / C / B (approx) |
|--------|---------|-------------------------|
| 50 | 72.22 / 71.59 | 77.15 / 66.65 / 71.91 / 5.25 |
| 60 | 65.97 / 65.48 | 69.75 / 61.70 / 65.73 / 4.03 |

Exact H/L bar selection is still approximate; behaviour above is the priority.

## Behaviour test

1. **Robot** + Extend 50 → note Decider  
2. Extend **60** → Decider **must change**  
3. Switch to **INDIAN** → note Decider  
4. Change Extend → Decider **must stay the same**; only line length changes  
