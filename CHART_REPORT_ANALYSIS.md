# Chart report analysis (`Chart_report_b194.pdf`)

Verified every row that includes Target 1 against the Decider ladder.

## Result

**Claim A (ladder algebra) is confirmed across the whole report** — Nifty, Sensex, Bank Nifty, Calls and Puts.

```
H = Target 1 upper
L = Target 1 lower
C = (H + L) / 2
B = (H − L) / 2
Decider High/Low = C ± 0.06 · B
```

| Contract | Vendor Decider | Predicted from T1 | Error |
|---|---|---|---:|
| Nifty 18Aug CE 24350 | 94.83 / 90.12 | 94.83 / 90.12 | ~0 |
| Nifty 18Aug PE 24350 | 67.61 / 65.24 | 67.61 / 65.24 | ~0 |
| Nifty 18Aug CE 24400 | 132.21 / 130.14 | 132.21 / 130.14 | ~0 |
| Nifty 18Aug PE 24450 | 137.23 / 135.47 | 137.23 / 135.47 | ~0 |
| Sensex 06Aug CE 78800 | 239.01 / 236.14 | 239.01 / 236.14 | ~0 |
| Sensex 06Aug PE 78800 | 211.84 / 206.86 | 211.84 / 206.86 | **exact** |
| Nifty 21Jul CE 24150 | 36.46 / 35.54 | 36.46 / 35.54 | ~0 |
| Nifty 21Jul PE 24200 | 39.34 / 38.51 | 39.34 / 38.51 | ~0 |
| Nifty 30Jun CE 23900 | 67.09 / 63.41 | 67.09 / 63.41 | ~0 |
| Nifty 30Jun PE 23950 | 31.11 / 28.89 | 31.11 / 28.89 | ~0 |
| BN 30Jun CE 57500 | 199.73 / 191.42 | 199.73 / 191.42 | ~0 |
| BN 30Jun PE 57800 | 167.15 / 160.10 | 167.15 / 160.10 | ~0 |

Implied Decider factor from the table is **0.0597–0.0604** → pins **0.06**.

Rows with **Decider only** (Nifty 14 Jul CE/PE 24100) still fit the same band; implied Target 1:

| Contract | Implied T1 (from Decider ÷ 0.06) |
|---|---|
| Nifty 14Jul CE 24100 | ~179.96 / 42.79 |
| Nifty 14Jul PE 24100 | ~149.93 / 47.42 |

---

## What this means (concept)

1. **Target 1 is the anchor pair** for that option contract that day.  
2. **Decider is not independent** — it is always the thin band `C ± 0.06B` around the midpoint of Target 1.  
3. **Targets 2–4** (when drawn) are the same midpoint expanded by **1.54 / 1.83 / 2.08 × B**.  
4. Same machine on **index, Sensex, Bank Nifty, CE, PE**.

### How to use it

- Trade plan is mirrored above/below the Decider.  
- Upper Target 1 / Lower Target 1 = the day’s reference range edges for that premium.  
- Wider B → wider Decider and farther T2–T4.

---

## What the report does *not* settle

**Where Target 1 (H/L) comes from on OPTIONS.**

Free NSE daily option OHLC (jugaad archive) does **not** match these Target 1 prints (same mismatch we saw earlier vs TradingView Daily on options).  

Separately, on the **Nifty index** screenshot, Target 1 matched **prior Close / prior Low**. That index finding must **not** be assumed for option premiums without a matching option OHLC feed.

Practical rule in our script:

| Chart | Recommended H/L source |
|---|---|
| **Index** | Prev Close + Prev Low (chart scan) |
| **Option CE/PE** | **Manual Target 1** = paste vendor T1 until auto matches your broker feed |

---

## Example rebuild (Nifty 18 Aug CE 24400)

```
H=148.35  L=114.00
C=131.175  B=17.175
Decider = 132.21 / 130.14     ✓ matches report
T2      = 157.62 / 104.73
T3      = 162.61 /  99.74
T4      = 166.90 /  95.45
```
