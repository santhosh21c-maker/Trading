# Decider & Targets — the actual concept

## What this system is

It is **not** Fibonacci of today’s candles and **not** CPR.

It is a **frozen daily ladder** built from two anchors (call them **H** and **L**):

1. Take two numbers from the **previous NSE session** of *this same chart symbol*.
2. Build a centre and a half-range.
3. Project a thin “Decider” band around the centre, then four mirrored targets each side.

```
C = (H + L) / 2          centre
B = (H − L) / 2          half-base

Decider  = C ± 0.06·B     thin decision zone
Target 1 = C ± 1.00·B     (= H and L themselves)
Target 2 = C ± 1.54·B
Target 3 = C ± 1.83·B
Target 4 = C ± 2.08·B
```

**How to read it**
- Price **above Decider** → working the upper ladder (bullish side of the day plan).
- Price **below Decider** → working the lower ladder.
- Target 1 is the edge of yesterday’s chosen range; T2–T4 are fixed expansions of that same base **B**.

---

## The one thing that can be wrong: what are H and L?

The ratios above are locked (verified to the tick on vendor prints).

**H and L are not “whatever Target 1 says” as a discovery — Target 1 is just those anchors plotted.**  
The real question is which prior-session statistics the vendor uses as H and L.

| Hypothesis | 14 Aug 2026 Nifty index vs vendor T1 24395.85 / 24311.45 |
|---|---|
| Prior **High / Low** | 24431.60 / 24311.40 → **FAIL** (H off ~36 pts) |
| Prior **Close / Low** | 24395.85 / 24311.40 → **PASS** |

So on that **index** chart, INDIAN anchors were:

```
H = previous session Close
L = previous session Low
```

Our script defaults to that (chart-bar scan first, Daily as fallback).  
If your chart still disagrees with the vendor, use **Manual Target 1** and paste the vendor’s two Target 1 numbers — the rest of the ladder will then match Claim A automatically.

---

## INDIAN vs Robot

| | INDIAN | Robot Prediction |
|---|---|---|
| Anchors | Prior session (Close/Low by default) | High/Low of a live `Extend` window |
| When levels change | Once per day (frozen) | When the window moves |
| `Extend` | Line length only | Changes the window → changes levels |

---

## Why lines appear at the open

Because INDIAN uses **yesterday’s** stats, the whole ladder is known before today’s opening range finishes. That is intentional.
