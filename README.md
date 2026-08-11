# Smart Robotic Logic – Decider & Targets

Educational Pine Script recreation of CPR-based **Decider** + mirrored **Target 1–4** levels (as seen on Nifty/Sensex option charts).

## Install on TradingView

1. Open [TradingView](https://www.tradingview.com) → chart
2. Bottom panel → **Pine Editor**
3. Paste contents of `Smart_Robotic_Logic_Decider_Targets.pine`
4. Click **Add to chart**

## Recommended settings (options)

| Setting | Suggested |
|--------|-----------|
| Chart | CE/PE premium, **1 minute** |
| Enable Automated Levels | On |
| Extend => Length | **50** (try **60** to see Decider shift) |
| CPR Mode | Current |
| Hybrid (Force 5 Min Values) | **On** |

## What it plots

- **Decider** (2 lines) = Central Pivot Range `TC` / `BC`
- **Target 1–4** above & below = `Pivot ± Range × multiplier`
- Labels match the screenshot style: `💔 Decider / price`, `😇 Target 1 / price`, etc.

## Formula (simple)

```
H, L, C = highest / lowest / close over Length (optionally on 5m)
P  = (H + L + C) / 3
BC = (H + L) / 2
TC = 2P − BC
Range = H − L

Upper Target N = P + Range × multN
Lower Target N = P − Range × multN
```

Changing **Length** 50 → 60 changes the H/L/C window → Decider moves → all Targets move with it.
