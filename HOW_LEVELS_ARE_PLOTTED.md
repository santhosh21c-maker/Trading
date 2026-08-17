# How Decider & Target levels are plotted

## Two separate claims (do not mix them)

| Claim | Status |
|---|---|
| **A. Ladder algebra** — once you have two anchors H≥L, Decider/Targets are `C±k·B` with fixed ratios | **Verified** (exact on vendor prints) |
| **B. What H and L are** — which session statistics become those anchors | **Must be tested against OHLC**, not inferred from Target 1 labels |

Claim A alone is not circular *as algebra*: it says the ten printed lines are one two-parameter family.  
Claim B is the only part that can be wrong — and for the **Nifty index** screenshot of 14 Aug 2026, the old wording “prior session high/low” **fails**.

---

## Claim A — Ladder (verified)

Given anchors **H** (upper Target 1) and **L** (lower Target 1):

```
C = (H + L) / 2
B = (H - L) / 2

Decider High/Low = C ± 0.06·B
Target n Upper/Lower = C ± Rn·B
```

| Level | Rn |
|---|---:|
| Target 1 | **1.00** (= H / L by definition of the anchors) |
| Target 2 | **1.54** |
| Target 3 | **1.83** |
| Target 4 | **2.08** |

### 14 Aug 2026 Nifty index (vendor print)

Anchors from Target 1 labels: **H = 24395.85**, **L = 24311.45**  
→ `C = 24353.65`, `B = 42.20`

| Level | Formula | Vendor | Match |
|---|---|---:|---|
| Decider | C±0.06B | 24356.18 / 24351.12 | exact |
| T1 | C±1.00B | 24395.85 / 24311.45 | exact (anchors) |
| T2 | C±1.54B | 24418.64 / 24288.66 | exact |
| T3 | C±1.83B | 24430.88 / 24276.42* | exact / ~0.3 |
| T4 | C±2.08B | 24441.43 / 24265.87 | exact |

\*Vendor lower T3 print ~24276.12 vs 24276.42 — mintick / rounding.

**Note on circularity:** Saying “Target 1 = H/L” is true *by how we named the anchors*. It does **not** prove where H/L came from. Ratios 0.06 / 1.54 / 1.83 / 2.08 are what Claim A actually establishes.

---

## Claim B — What are H and L? (**OPEN — not settled**)

Reproducing Decider from Target 1 only confirms Claim A. It does **not** explain the vendor’s anchors.

### Put-call structure (missed earlier; now verified)

Same-strike CE+PE are **one index ladder**, not two puzzles:

```
Ci = K + (Cc − Cp)      // index centre
Bi = Bc + Bp            // index base
```

Report checks: Nifty 24350 → Ci=24376.050, Bi=59.050; Sensex 78800 → 78828.225 / 65.375 (exact).

### Prior Close/Low — withdrawn as a general claim

- Matched **one** direct Nifty index screenshot (14 Aug T1 = prior Close/Low).  
- Fails on option OHLC.  
- Fails on the **put-call-reconstructed** index ladder from the 24350 pair (T1≈24435/24317 ≠ Close/Low).  

Treat Close/Low as a failed-or-partial hypothesis, not the answer.

**Practical:** paste vendor Target 1 into **Manual H/L**. Research H/L provenance separately (prefer the put-call index view).

---

## Segments (unchanged idea)

| Segment | Anchors | Behaviour |
|---|---|---|
| **INDIAN** | Prior session stats of *this* symbol (see Claim B) | Frozen for the day. `Extend` = line length only. |
| **Robot Prediction** | High/Low of a live `Extend` window | Same ladder ratios; window changes levels. |

---

## How this script should be used

1. Treat **ratios** (Claim A) as solid.  
2. Pick an **H/L source** explicitly; do not assume “prior High/Low”.  
3. For Nifty **index**, prefer **Prev Close + Prev Low** until a counter-example appears.  
4. If auto anchors disagree with the vendor, set **Manual Target 1** to the vendor’s T1 High/Low and the rest of the ladder will follow Claim A.

---

## Quick self-check

1. Read vendor Target 1 High/Low → those are anchors H, L.  
2. Recompute Decider with `C±0.06B` and T2–T4 with 1.54 / 1.83 / 2.08.  
3. Separately compare H, L to prior Close/Low/High from the exchange — that tests Claim B only.
