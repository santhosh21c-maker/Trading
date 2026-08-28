# Option TBT chart horizontals — reverse engineering

**Constraint:** lines appear **before market open** → prior session only.

## Response to the corrected critique (28 Aug)

### Spot auction note — **correct**

Official Nifty archive for 27 Aug has `L = C = 24090.85` (closing-auction print).  
Your **traded** session `H = 24297.45`, `L = 24120.60`, `C = 24090.85` rebuilds classic CPR exactly as you listed (R2…S2). On that down-close day `BC > TC`, so “CPR top/bottom” are the higher/lower band edges (`24209.03` / `24130.24`), not the names TC/BC in isolation.

That spot CPR still sits near **24,100+**. It is the right spot ladder; it is **not** the premium horizontals (~50–200) on the option TBT pane.

---

### Claim 1 — green ≈ option previous close — **agreed, solid**

| Contract | Prior | NSE CLOSE/SETTLE | NSE LTP | Green | Δ to settle |
|---|---|---:|---:|---:|---:|
| 24150 PE | 27 Aug | 78.95 | 88.70 | 79.20 | +0.25 |
| 24200 CE | 24 Aug | 160.00 | 158.25 | 159.55 | −0.45 |
| 24200 PE | 24 Aug | 121.35 | 129.75 | 123.30 | +1.95 |
| 24250 PE | 26 Aug | 67.85 | 75.10 | 69.60 | +1.75 |

Green tracks the **option’s prior session close reference**, not spot. Small gaps are settle / header / label noise — not a second model.

Note: for 24200 CE, `158.25` in the ratio table is the day’s **LTP**, not settle (`160.00`). Green still sits on the close cluster either way. Claim 1 stands.

---

### Claim 2 — red = option CPR bottom `(H+L)/2` — **not from IV; exchange Daily settles it**

Your caution about **IV-reconstructed** option H/L is right: ±1 vol point ≈ 6–10 premium points of noise, so that method **cannot** reject or confirm Claim 2.

But Claim 2 in this repo was **not** built that way. It used **NSE FO daily High/Low** for that contract (same numbers the Daily candle shows — your ten-second check):

| Contract | Prior | FO High | FO Low | `(H+L)/2` | Red | Δ |
|---|---|---:|---:|---:|---:|---:|
| 24150 PE | 27 Aug | 95.00 | 33.40 | **64.20** | 64.30 | **0.10** |
| 24200 CE | 24 Aug | 241.60 | 146.05 | **193.82** | 193.85 | **0.03** |
| 24200 PE | 24 Aug | 141.60 | 67.20 | **104.40** | 104.70 | **0.30** |
| 24250 PE | 26 Aug | 84.35 | 36.55 | **60.45** | 60.50 | **0.05** |

With real prior option H/L, red locks to **BC**.  
IV reconstruction midpoints (~54–187) disagree because they are **not** the option’s traded H/L — that gap is reconstruction error, not evidence against BC.

**Verdict:** Claim 2 is **confirmed on exchange FO Daily OHLC**. Still worth eyeballing once on the broker Daily candle; it should match the table above.

---

### Claim 3 — 24250 PE red 116.50 = `C+(H−L)` — **plausible on FO OHLC**

| Source | H | L | C | `C+(H−L)` | vs 116.50 |
|---|---:|---:|---:|---:|---:|
| NSE FO 26 Aug | 84.35 | 36.55 | 67.85 | **115.65** | Δ **0.85** |
| IV reconstruction | — | — | — | ~108.10 | weaker |

Your weaker footing applies to the **reconstruction**. On exchange OHLC the identity is close (same order as label rounding). Treat as **likely**, second red = range projection from prior close.

---

### Purples = Camarilla / fibs — **your caution stands**

Worst-errors of 10–32 pts from reconstructed H/L mean that path cannot prove Camarilla/fibs.  
Even on FO OHLC, only **some** purples sit near Camarilla/fib prints (e.g. 24150 CR4/CR2); it is **not** a clean full-ladder proof. “Looks unlikely as the whole purple system” is fair; not fully falsified without the indicator name.

---

## Bottom line

| Item | Your take | Ours after re-check |
|---|---|---|
| Spot 15:25 auction / traded low | Correct | Agreed |
| Corrected spot CPR table | Correct | Agreed (spot only) |
| Claim 1 green = opt prev close | Solid | **Agreed** |
| Claim 2 red = opt BC via IV recon | Unresolved / don’t overfit | IV path unresolved **by design**; **FO Daily H/L confirms BC** |
| Claim 3 `C+(H−L)` | Weaker on recon | **~115.65 vs 116.50** on FO OHLC |
| Purples Camarilla/fib | Unlikely / not proven | Agreed — not a locked pack |

**Pre-open recipe that survives this review:** for each option, from **that contract’s prior Daily candle**: plot **Close** (green) and **`(H+L)/2`** (red). Optional: `C+(H−L)` for the upper red when present.

```bash
python3 verify_option_chart_levels.py
```
