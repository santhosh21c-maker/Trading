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

## Segments

| Segment | What Length does | H / L source |
|---------|------------------|--------------|
| **INDIAN** | Visual line extend only | Prior calendar day H/L (Hybrid 5m optional) |
| **Robot Prediction** | Changes Decider/Targets **and** extends lines forward | Chart TF (use **1m**). Today only, after **Robot Start HHMM** |

## Why Length 50 showed L ≈ 33

Hybrid 5m + Length pulled the **open crash** (and older bars) into the low. Length 50’s **H ≈ 77.55** was already near the vendor; only **L** was wrong. Length 60’s C looked closer only because a huge H and tiny L averaged near the vendor midpoint — **B was still far too wide**.

Robot now **ignores Hybrid** for H/L and skips bars before **Start HHMM** (default `1000` = 10:00 IST).

## Vendor Robot targets (PUT 24500 reference)

| Length | Decider (approx) | Implied C / B / H / L |
|--------|-------------------|------------------------|
| 50 | 72.22 / 71.59 | C≈71.90 B≈5.25 H≈77.15 L≈66.65 |
| 60 | 65.97 / 65.48 | C≈65.73 B≈4.08 H≈69.76 L≈61.69 |

## Install / test

1. TradingView → Pine Editor → paste `Smart_Robotic_Logic_Decider_Targets.pine`
2. Chart: **1-minute** CE/PE (Replay OK)
3. Segment = **Robot Prediction**
4. Defaults: Window = **Last Length bars**, Start HHMM = **1000**, bodies **off**
5. Change Length at the comparison time → status chip must show **FROZEN** with new H/L/C/B
6. If L is still too low, raise Start to `1015` / `1030`. If H/L are too tight/loose, try **Shifted [Len, 2Len)** or bodies on.

## Still approximate

Exact vendor bar selection is closed-source. Ladder math after H/L is locked; we are tuning the Robot window so Len 50/60 match the table above.
