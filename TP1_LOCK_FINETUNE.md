# TP1 Lock fine-tune — capture +10 before SL

## Goal
Maximize share of trades that print **+10 premium points** before stop (CE and PE).

## Best config found
```json
{"min_score": 5, "sl": 30, "require_E7": true, "require_E3": true, "hold_to_tp1": true, "exit_full_at_tp1": true, "n": 12, "tp1_first_pct": 91.7, "net": 80.0, "avg": 6.67}
```

## Notes
- Cannot reach 100% with a finite SL; remaining ~8% are adverse moves that never tag +10.
- SL=10 on the same strict entries → ~0% TP1-first (stop hits first on this sample).
- Implemented as defaults in `Nifty_Options_Confluence.pine` v1.1.
