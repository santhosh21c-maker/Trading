# Nifty Options Confluence v1.1 — SL=18

## Defaults now

| Setting | Value |
|---------|--------|
| SL | **18** |
| TP1 / TP2 / TP3 | **10 / 20 / 35** |
| TP1 lock (full exit at +10) | **OFF** — use runners |
| Hold to TP1 | ON |
| After TP1 | SL → breakeven |
| After TP2 | trail to entry+½·TP1 |
| Min BUY score | **5** + require **E7** and **E3** |

## SL=18 backtest snapshot (40 contracts · Apr–Jul 2025)

| | Runners | TP1 lock |
|--|--------:|---------:|
| Trades | 128 | 130 |
| Reach TP1 | **48 (38%)** | 49 (38%) |
| Reach TP2 | **41 (32%)** | — |
| Reach TP3 | **35 (27%)** | — |
| SL exits | **80 (63%)** | 81 (62%) |
| Calls / signal-day | **~1.2** | ~1.2 |
| ATM calls / session-day | **~0.13** | ~0.13 |
| Net | −185 (ATM only **+14**) | **−968** |

Full tables: `BACKTEST_SL18_REPORT.md`

## How to use

1. Open Nifty CE/PE (3m/5m).
2. Paste `Nifty_Options_Confluence.pine`.
3. Leave **TP1 lock OFF**, **SL=18**, runners BE/trail ON.
