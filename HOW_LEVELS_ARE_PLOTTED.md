# How Decider & Target levels are plotted

Verified on PxTrading **Smart Robotic Logic – INDIAN** screenshots (12 Aug & 13 Aug 2026 option charts).

## Step 1 — Choose H and L

| Segment | What is H / L? |
|---|---|
| **INDIAN** | **Prior session day High / Low** of the *same* symbol (that Call/Put/Index). Frozen for the whole day from the open. `Extend` only changes how long the lines are drawn. |
| **Robot Prediction** | High / Low of a **live** bar window controlled by `Extend` (opening-range clock, last-N bars, etc.). |

**Important:** Session *today’s* High/Low labels on the chart (e.g. High 148.50 / Low 97.00) are **not** the ladder H/L. Ladder H/L = **Target 1** = **yesterday’s NSE session (09:15–15:30 IST)** high/low of that option.

**Do not use raw TradingView Daily OHLC on NSE options** — it often disagrees with the vendor (example: Daily gave 214/100 while vendor Target 1 was 148.33/114). Use **Chart TF session** or **Hybrid 5m session** scan instead.

### Today’s CALL example (Nifty 18 AUG CE 24400)
- Ladder **H = 148.33**, **L = 114.00** (= Target 1 High / Low)
- Decider 132.21 / 130.14, Targets match the ratios below

### Today’s PUT example (Nifty 18 AUG PE 24450)
- From Decider 137.23 / 135.47 → **H ≈ 151.02**, **L ≈ 121.68** (= Target 1)

---

## Step 2 — Centre C and Base B

```
C = (H + L) / 2
B = (H - L) / 2
```

CALL today: `C = 131.165`, `B = 17.165`

---

## Step 3 — Decider band (pink / red dotted)

```
Decider High = C + 0.06 × B
Decider Low  = C − 0.06 × B
```

CALL: `131.165 ± 1.03` → **132.19 / 130.14** (vendor shows 132.21 / 130.14 — mintick rounding)

This is a thin “decision” zone around the midpoint — not a Fibonacci of today’s range.

---

## Step 4 — Targets 1–4 (above and below)

```
Upper Target n = C + Rn × B
Lower Target n = C − Rn × B
```

| Level | Ratio Rn | CALL today (H=148.33, L=114) |
|---|---|---|
| Target 1 | **1.00** | **148.33 / 114.00** (= H / L) |
| Target 2 | **1.54** | **157.60 / 104.73** |
| Target 3 | **1.83** | **162.58 / 99.75** |
| Target 4 | **2.08** | **166.87 / 95.46** |

Vendor labels on the stream match these within a few ticks.

---

## Why levels exist at 09:xx before any opening range

Because **INDIAN** uses **prior-day** H/L, the whole ladder is known at the open.  
If it used today’s OR freeze (e.g. 09:20–09:50), levels could not be fully drawn that early.

---

## Quick check on any option chart

1. Look at **Target 1 High / Low** on the vendor.  
2. Those two numbers **are** H and L.  
3. Recompute Decider with `C ± 0.06×B` — it should match.  
4. Recompute T2–T4 with 1.54 / 1.83 / 2.08 — it should match.

---

## Robot Prediction (different H/L, same ladder)

Same Decider/Target **ratios**. Only the **window** that produces H/L changes when you move `Extend` (e.g. Ext50 → clock OR 09:30–10:05 IST with int time math).
