# Decider & Targets — the actual concept

## What this system is

A **frozen daily ladder** from two anchors **H ≥ L**:

```
C = (H + L) / 2
B = (H − L) / 2

Decider  = C ± 0.06·B
Target 1 = C ± 1.00·B   (= H / L)
Target 2 = C ± 1.54·B
Target 3 = C ± 1.83·B
Target 4 = C ± 2.08·B
```

Above Decider → upper side of the plan; below → lower side.

**Important:** Showing that Decider follows from Target 1 only proves these ratios.  
It does **not** explain where the vendor got H and L.

## Put-call (same strike)

A call and put at strike **K** encode one **index** ladder:

```
Ci = K + (Cc − Cp)
Bi = Bc + Bp
```

(Verified on the chart report for Nifty 24350 and Sensex 78800.)

## H/L source = open

Prior High/Low and prior Close/Low are **hypotheses**, not proven.  
Close/Low matched one index screenshot and then failed other tests — **withdrawn** as the answer.

**To match the vendor:** paste Target 1 into **Manual H/L**.
