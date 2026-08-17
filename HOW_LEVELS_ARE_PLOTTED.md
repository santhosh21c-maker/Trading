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

## Claim B — What are H and L? (corrected)

### Falsification of “prior session High / Low” on this index chart

NSE Nifty 50 official daily:

| Date | Open | High | Low | Close |
|---|---:|---:|---:|---:|
| 2026-08-12 | 24472.45 | 24473.30 | 24265.95 | 24435.95 |
| 2026-08-13 | 24431.60 | **24431.60** | **24311.40** | **24395.85** |
| 2026-08-14 | 24361.90 | 24405.20 | 24296.80 | 24366.00 |

14 Aug vendor Target 1 = **24395.85 / 24311.45**.

| Hypothesis | Predicted T1 | vs vendor | Result |
|---|---|---|---|
| Prior **High / Low** (13 Aug) | 24431.60 / 24311.40 | H off by **+35.75** | **FAIL** |
| Prior **Close / Low** (13 Aug) | 24395.85 / 24311.40 | H exact, L within 0.05 | **PASS** (this sample) |

So on **this index chart**, INDIAN anchors behave as:

```
H = prior NSE session Close
L = prior NSE session Low
```

not prior High/Low.

### Why “13 Aug candles pierce T1” does not settle Claim B

Vendor lines are usually **today’s frozen ladder drawn across history**.  
14 Aug’s T1 band painted leftward over 13 Aug bars will be crossed by 13 Aug price without contradiction.  
The OHLC test above is the proper falsifier.

### Options charts (earlier work)

On CE/PE screenshots we matched Target 1 labels to a prior-session premium range and verified Claim A the same way.  
Whether that option range was High/Low vs Close/Low was **not** locked with exchange OHLC in the same way as this index test. Treat option H/L source as **still open** until checked the same way.

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
