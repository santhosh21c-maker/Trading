# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of the PxTrading-style **Decider / Target** ladder.

## Ladder formula (verified)

```text
C = (H + L) / 2
B = (H - L) / 2
Decider  = C ± 0.06·B          // gap = 0.12·B
Target 1 = C ± 1.00·B
Target 2 = C ± 1.54·B
Target 3 = C ± 1.83·B
Target 4 = C ± 2.08·B
```

## Extend = line length only

Under **Robot Prediction**, Extend only lengthens the **horizontal** Decider/Target lines. It does **not** plot a future price path, and it does **not** change C/B.

## Segments

| Segment | H / L source | Extend |
|---------|--------------|--------|
| **INDIAN** | Prior calendar day | Visual only |
| **Robot Prediction** | Configurable (default: today after Start, H=body high, L=low) | Visual only |

## Vendor reference (11 Aug 2026, Robot Prediction)

| Contract | Extend (visual) | Decider | Implied H / L / C / B |
|----------|-----------------|---------|------------------------|
| CALL 24450 | 60 | 34.77 / 33.18 | H≈47.30 L≈20.65 C≈33.98 B≈13.33 |
| PUT 24450 | 50 | 13.5 / 12.9 | H≈18.15 L≈8.25 C≈13.20 B≈4.95 |

Note: our earlier PUT run matched **L=8.25** but **H=32.15** (upper wick). Default Robot H source is now **Body high**.

## Install / test

1. Paste `Smart_Robotic_Logic_Decider_Targets.pine` on **1m** CE/PE
2. Segment = **Robot Prediction**
3. Defaults: Range = **Today after Start**, H = **Body high**, L = **Low**, Start = **915**
4. Toggle **Force Recalculate** once after load
5. Compare status chip H/L/C/B to the table above
6. If H still high, try H source **Close**, or Range **Last N bars** / **Prior day**

## Still approximate

Exact vendor bar selection is closed-source. Ladder math after H/L is locked.
