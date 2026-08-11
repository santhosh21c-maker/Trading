# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of the PxTrading-style **Decider / Target** ladder.

## Extend = line length only

Under **Robot Prediction** (and Indian), **Extend** only lengthens horizontal Decider/Target lines.

- It does **not** change H / L / C / B / Decider / Targets
- It does **not** plot a future price path

## Ladder (verified)

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B
Target N = C ± {1.00, 1.54, 1.83, 2.08}·B
```

## H / L sources

| Segment | H/L source | Extend |
|---------|------------|--------|
| **INDIAN** | Prior calendar day | Lines only |
| **Robot Prediction** | **Opening Range** (default): Start HHMM + OR Minutes — *not* Extend — or Prior day | Lines only |

## Vendor reference (Robot Prediction, 11 Aug 2026)

| Contract | Extend (visual) | Decider | H / L / C / B |
|----------|-----------------|---------|----------------|
| CALL 24450 | 60 | 34.77 / 33.18 | 47.30 / 20.65 / 33.98 / 13.33 |
| PUT 24450 | 50 | 13.5 / 12.9 | 18.15 / 8.25 / 13.20 / 4.95 |

## Test

1. Paste script on 1m CE/PE  
2. Segment = Robot Prediction  
3. Change **Extend** 50 ↔ 60 → lines move, **C/B must stay the same**  
4. Tune **OR Minutes** / Start (or switch to Prior day) until H/L match the table  
5. Toggle Force Recalculate after recipe changes; send status-chip H/L/C/B  
