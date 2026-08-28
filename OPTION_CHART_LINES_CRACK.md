# Option TBT chart horizontals — reverse engineering

**Constraint confirmed by you:** lines appear **before market open** → they can only use **previous session** data (option and/or spot). No live session H/L.

## Verdict (re-checked)

| Claim | Result |
|---|---|
| Pre-open ⇒ prior-day inputs only | **Agreed — used as hard constraint** |
| Decider / Targets ladder | **Falsified** |
| Raw **Nifty spot** CPR/pivots (~24100–24300) plotted as-is | **Impossible** (wrong scale vs premium ~50–200) |
| Spot → PE/CE **intrinsic** of spot CPR | **Fails** for green/red on the main shots |
| **Option premium prior-day** OHLC | **Fits green + red** |
| Green | **≈ previous day close (PDC)** of that option |
| Red (the mid one) | **= CPR BC = (prior High + prior Low) / 2** of that option |
| Purple / black full set | **Partially** Camarilla / fib / classic from **same option prior day**; not uniquely named yet |

---

## Re-check method

1. Pull NSE FO daily OHLC for the exact contracts (jugaad).  
2. Pull Nifty 50 daily OHLC for the same prior dates.  
3. For each chart level, allow **only** formulas from that prior day (PDC/PDH/PDL, CPR, classic pivots, Camarilla, fib-of-prior-range).  
4. Compare **option-premium** pack vs **spot→intrinsic/dist** pack.

Reproduce:

```bash
python3 verify_option_chart_levels.py
```

---

## Proof table — Green = opt PDC, Red = opt BC

| Chart | Prior day | Opt PDC | Green | Δ | Opt BC | Red | Δ |
|---|---|---:|---:|---:|---:|---:|---:|
| 24150 PE | 27 Aug | 78.95 | 79.20 | **0.25** | 64.20 | 64.30 | **0.10** |
| 24250 PE | 26 Aug | 67.85 | 69.60 | 1.75 | 60.45 | 60.50 | **0.05** |
| 24200 PE | 24 Aug | 121.35 | 123.30 | 1.95 | 104.40 | 104.70 | **0.30** |
| 24200 CE | 24 Aug | 160.00 | 159.55 | **0.45** | 193.82 | 193.85 | **0.03** |

Formula:

```
PDC = prior Close
BC  = (prior High + prior Low) / 2
```

Green Δ of ~1.7–2.0 on two PE charts is likely label rounding / LTP-vs-settle / screenshot read — still far closer than any spot-intrinsic candidate (typically 5–20 pts off).

---

## Why not spot chart data?

Nifty prior CPR lives near **24,200**, e.g. 27 Aug:

| Spot level | Value |
|---|---:|
| PDC | 24090.85 |
| PP | 24159.72 |
| BC | 24194.15 |

Those numbers cannot be the horizontals on an option premium pane (~50–200).

Converting spot levels to PE intrinsic `max(K − spot, 0)` also **misses** the 24150 green/red (e.g. intr(PDC)=59.15 vs green 79.20). So these lines are **not** spot CPR painted through intrinsic.

One coincidence only: on 24200 CE, red 193.85 ≈ both **opt BC (193.82)** and spot R2 intrinsic (~194.15). Green still locks to **opt PDC**, so the coherent story remains **option prior-day CPR + PDC**.

---

## Extra red / purples (still prior-day option)

| Chart | Level | Best prior-day option formula | Δ |
|---|---:|---|---:|
| 24250 PE | red 116.50 | C + (H−L) | 0.85 |
| 24150 PE | purple 113.25 | Camarilla R4 | 0.42 |
| 24150 PE | purple 89.70 | Camarilla R2 | 0.54 |
| 24150 PE | purple 132.40 | L + 1.618·(H−L) | 0.67 |
| 24150 PE | black 122.35 | C + 0.705·(H−L) | 0.03 |

Same-name list does **not** lock every purple on every strike with official OHLC → likely a **multi-pivot pack** (CPR + Camarilla + fibs) and/or some **manual Elite Circle** rays on top. Needs indicator name from the chart object tree to finish.

---

## Practical pre-open recipe

On each option chart, before 9:15, from **that contract’s yesterday OHLC**:

1. Plot **PDC** (your green).  
2. Plot **BC = (H+L)/2** (your mid red).  
3. Optionally add Camarilla R1–R4 / S1–S4 and classic R1–R2 (candidate purples).

That matches how the lines can exist **before the open** with no live bar yet.
