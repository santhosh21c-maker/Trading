# Option chart horizontals — corrected logic

## Actual logic (pre-open)

Lines are drawn from **that option contract’s previous Daily candle** (NSE FO OHLC), not from Decider/Targets and not from raw Nifty spot CPR.

| Color / role | Formula | Status |
|---|---|---|
| **Green** | `Previous Close` `C` | **Confirmed** |
| **Red (mid / CPR edge)** | `BC = (H + L) / 2` | **Confirmed** on exchange FO Daily H/L |
| **Red (upper, when present)** | `C + (H − L)` | **Likely** (24250: 115.65 vs 116.50) |
| CPR pivot / top (often drawn too) | `P = (H+L+C)/3`, `TC = 2P − BC` | Same input set; may be other colours |
| **Purple / black** | Not a single proven Camarilla/fib pack | **Unresolved** — see below |

```
Inputs: prior session High H, Low L, Close C  of THIS option

P  = (H + L + C) / 3
BC = (H + L) / 2
TC = 2·P − BC          // if TC < BC, visual CPR top = BC, bottom = TC

Green = C
Red   = BC
Red₂  = C + (H − L)    // optional range projection
```

All of that is known **before 9:15**.

---

## Proof (exchange FO Daily — not IV reconstruction)

| Contract | Prior | H | L | C | BC | Green | ΔC | Red | ΔBC |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 24150 PE | 27 Aug | 95.00 | 33.40 | 78.95 | 64.20 | 79.20 | 0.25 | 64.30 | 0.10 |
| 24250 PE | 26 Aug | 84.35 | 36.55 | 67.85 | 60.45 | 69.60 | 1.75 | 60.50 | 0.05 |
| 24200 PE | 24 Aug | 141.60 | 67.20 | 121.35 | 104.40 | 123.30 | 1.95 | 104.70 | 0.30 |
| 24200 CE | 24 Aug | 241.60 | 146.05 | 160.00 | 193.82 | 159.55 | 0.45 | 193.85 | 0.03 |

24250 upper red: `C+(H−L) = 115.65` vs **116.50** (Δ 0.85).

On 24200 CE the prior close sits near the low, so `BC > TC`; the **visual CPR top** is BC — same number as red.

---

## Corrections vs earlier / IV critique

| Topic | Correction |
|---|---|
| Spot 15:25 = auction | Agree. Traded low 24,120.60 rebuilds **spot** CPR; that ladder is ~24k and is **not** the premium lines. |
| Claim 1 green = opt prev close | **Keep.** |
| Claim 2 via IV-reconstructed H/L | Rightly inconclusive (±1 vol ≈ 6–10 pts). |
| Claim 2 via FO Daily H/L | **Keep — confirmed.** Same as reading the prior Daily candle. |
| Claim 3 `C+(H−L)` via IV recon | Weak. Via FO OHLC: **likely**. |
| Purples = Camarilla / fibs | **Not established.** Partial hits only; do not treat as the system. |

---

## What purple / black are *not* (so far)

Tested against real prior option H/L/C and rejected as a full explanation:

- Decider / Targets (`C ± k·B`)
- Raw spot CPR / classic spot pivots
- Spot → intrinsic of spot CPR
- Weekly option CPR
- Pure Camarilla R1–R4 / S1–S4 as the whole purple set
- Pure fib pivots as the whole purple set

Some purples sit near Camarilla or CPR-width multiples on individual charts; that is **coincidence-level**, not a locked pack. Treat extra purple/black rays as **vendor/manual S/R** until the indicator name is known.

---

## How to verify in ten seconds (broker)

1. Open the **same option** → switch to **Daily**.  
2. Read previous candle `H`, `L`, `C`.  
3. Check:
   - green ≈ `C`
   - red ≈ `(H+L)/2`
   - any upper red ≈ `C+(H−L)`

Or run:

```bash
python3 verify_option_chart_levels.py
```

Or add `Option_PreOpen_CPR.pine` on the option chart (Daily-based levels, extends into the session).

---

## Practical use

Pre-open on each CE/PE you trade:

1. Bias magnet: **yesterday’s close** (green).  
2. Midrange decision: **BC** (red) — break/hold of prior day’s halfway premium.  
3. Stretch: **C + range** if your layout shows the second red.  
4. Do **not** assume purples are Camarilla targets without confirming the script.
