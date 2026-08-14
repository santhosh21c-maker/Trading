# SmartFlow Gold Suite — Quality Check (v4.0 → v4.1)

Verdict: **solid architecture, not “perfect.”** Engines are well separated and the ENABLE / draw / score model is sound. The chart clutter and a few logic bugs are real.

## What is good

- **17 engines with clear roles** — scoring vs gates vs output is coherent.
- **Adaptive max score** — turning an engine off does not silently lower the bar.
- **BUY-only with bear veto** — intentional and consistent (no sell path).
- **OB real candle bounds** — correct fix vs normalised ATR boxes.
- **FVG close-through-mid mitigation** — better than wick-kill for gold.
- **Quiet compute / optional draw** — right idea; defaults were still too busy on a 5m chart.

## Why your chart looks clumsy

From the screenshot, these are stacking on top of each other:

| Layer | Clutter impact |
|-------|----------------|
| Order Blocks + FVG boxes | Highest — overlapping translucent zones |
| LIQ / Supply-Demand shelves + labels | High — long right-edge tags |
| BOS / CHoCH on every break | High — label spam |
| SWEEP + SURESHOT | Medium |
| POC / VAH / VAL + CPR + round numbers | Medium — line forest |
| Right-edge level tags | Low–medium |

Even with some draws “OFF by default,” **Signal Focus clutter** still comes from FVG + Structure + Sweeps + VP + CPR + rounds all drawing together. One master **Chart Mode** is required so you are not hunting 17 Draw toggles.

## Bugs / correctness issues found in v4.0

1. **`f_obAge` never used** — OB strength always adds a flat `+2.0` “freshness.” Age decay was written but not wired in.
2. **E7 magnets always `box.new` / `label.new`** — even with Draw OFF. Burns the 500-object budget (E5 already avoided this; E7 did not).
3. **E8 chart-TF FVG** — `f_addZone(cBg, …)` without `f_isNew` can re-add / churn while the gap persists.
4. **HTF bias + CPR use `lookahead_on`** — partially offset with `[1]`, but still a repaint risk on live HTF updates. v4.1 switches bias/CPR reads to `lookahead_off` where safe.
5. **Structure after BOS** — clearing `lastSwingHigh` / `lastSwingLow` to `na` drops the opposite swing memory; structure can flicker.
6. **Order flow is not footprint** — correctly documented; do not treat Δ as true bid/ask.
7. **News Guard cannot know CPI/FOMC** — manual times must be updated; auto NFP + spike only.

## What “perfect” would still need (outside Pine)

- True footprint / DOM (Pine cannot do this).
- Live economic calendar API (Pine cannot do this).
- Walk-forward validation of E16 thresholds on your broker’s XAUUSD feed.

## v4.1 cleanup (this branch)

- Master **Chart Mode**: Clean Chart · Signal Focus · Full Study · Custom.
- Quieter Signal Focus defaults (1 FVG/side, Sureshot-only labels, POC without VAH/VAL, majors-only rounds, BOS off / CHoCH optional).
- Fixes for OB age, E7 object creation, chart-TF FVG `f_isNew`, safer HTF lookahead.
- Engines remain separate (E1–E17 groups unchanged in role).
