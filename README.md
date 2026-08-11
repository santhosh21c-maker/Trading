# Smart Robotic Logic – Decider & Targets

Educational Pine recreation of the PxTrading-style **Decider / Target** ladder.

## What your 7 screenshots proved

| # | Segment | Length | Result |
|---|---------|--------|--------|
| 1–2 | INDIAN | 80 | One frozen ladder (PUT C≈39.53, B≈8.78) |
| 3 | → Robot Prediction | 80 | Segment change → entirely different C/B |
| 4–5 | Robot Prediction | 50 | New frozen ladder (PUT C≈71.91, B≈5.25) |
| 6–7 | Robot Prediction | 60 | New frozen ladder (PUT C≈63.35, B≈3.85) |

**Remembered rules**
1. Levels are **static** — they do not move with each candle; they only change when **Segment** or **Length** changes.
2. Price often reacts at these lines (your observation).
3. **INDIAN** and **Robot Prediction** are different C/B recipes; the ladder ratios afterward are the same.

## Ladder formula (verified)

```text
Decider  = C ± 0.06·B          // gap = 0.12·B
Target 1 = C ± 1.00·B
Target 2 = C ± 1.54·B
Target 3 = C ± 1.83·B
Target 4 = C ± 2.08·B
```

## Install

1. TradingView → Pine Editor → paste `Smart_Robotic_Logic_Decider_Targets.pine`
2. Add to CE/PE chart (1m), **Hybrid 5m ON**
3. Set **Segment** + **Length** to match the vendor script
4. Tune **Robot – B = Range ×** or **Indian – B = Range ×** until Target 1 matches
5. Status chip shows `FROZEN` — levels stay put until you change Segment/Length (or toggle Force Recalculate)

## Still approximate

Exact vendor recipe for **how C and B are taken from Length** (which bars, which series) is closed-source. This script snapshots a Length-window pivot/range when inputs change, then freezes — matching the static behaviour you documented.
