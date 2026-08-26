#!/usr/bin/env python3
"""Fetch live NSE index option-chain OI and bake walls into Strike_Rate.pine.

TradingView Pine cannot call the internet. This bridge pulls OI from NSE
(via jugaad_data) and writes:
  - oi_walls.json
  - updates the ONLINE OI block inside Strike_Rate.pine

Usage:
  python3 fetch_oi_walls.py              # NIFTY nearest expiry
  python3 fetch_oi_walls.py BANKNIFTY
  python3 fetch_oi_walls.py NIFTY --expiry 25-08-2026
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from jugaad_data.nse import NSELive

ROOT = Path(__file__).resolve().parent
PINE = ROOT / "Strike_Rate.pine"
OUT = ROOT / "oi_walls.json"

MARK_BEGIN = "// === ONLINE_OI_BEGIN (auto-filled by fetch_oi_walls.py) ==="
MARK_END = "// === ONLINE_OI_END ==="


def fetch(symbol: str, expiry: str | None):
    live = NSELive()
    raw = live.index_option_chain(symbol.upper())
    records = raw.get("records") or {}
    spot = float(records.get("underlyingValue") or 0)
    expiries = records.get("expiryDates") or []

    # Prefer filtered (nearest) unless a specific expiry is requested
    if expiry:
        # Accept 18-Aug-2026 or 18-08-2026
        rows = []
        for r in records.get("data") or []:
            ce, pe = r.get("CE") or {}, r.get("PE") or {}
            ed = (ce.get("expiryDate") or pe.get("expiryDate") or "")
            if _exp_match(ed, expiry) or _exp_match(r.get("expiryDate") or "", expiry):
                rows.append(r)
        exp_used = expiry
    else:
        rows = (raw.get("filtered") or {}).get("data") or []
        exp_used = None
        if rows:
            sample = (rows[0].get("CE") or rows[0].get("PE") or {})
            exp_used = sample.get("expiryDate")
        if not exp_used and expiries:
            exp_used = expiries[0]

    ces, pes = [], []
    for r in rows:
        k = r.get("strikePrice")
        ce, pe = r.get("CE") or {}, r.get("PE") or {}
        if expiry and ce and not _exp_match(ce.get("expiryDate") or "", expiry):
            ce = {}
        if expiry and pe and not _exp_match(pe.get("expiryDate") or "", expiry):
            pe = {}
        if ce:
            ces.append({
                "strike": int(k),
                "oi": int(ce.get("openInterest") or 0),
                "chg": int(ce.get("changeinOpenInterest") or 0),
            })
        if pe:
            pes.append({
                "strike": int(k),
                "oi": int(pe.get("openInterest") or 0),
                "chg": int(pe.get("changeinOpenInterest") or 0),
            })

    ces.sort(key=lambda x: x["oi"], reverse=True)
    pes.sort(key=lambda x: x["oi"], reverse=True)
    if not ces or not pes:
        raise SystemExit(f"No OI rows for {symbol} expiry={exp_used!r}")

    resistance = ces[0]
    support = pes[0]
    # If both walls pin the same ATM strike, expose the next distinct wall so S≠R
    if resistance["strike"] == support["strike"]:
        for c in ces[1:]:
            if c["strike"] != support["strike"]:
                resistance = c
                break
        for p in pes[1:]:
            if p["strike"] != ces[0]["strike"] and p["strike"] != resistance["strike"]:
                # keep primary max-PE as support; only shift if we want spread — keep support as top PE
                break

    return {
        "symbol": symbol.upper(),
        "spot": spot,
        "expiry": exp_used,
        "fetched_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "resistance": resistance,  # max call OI (or 2nd if tied with put wall)
        "support": support,        # max put OI
        "magnet": ces[0] if ces[0]["strike"] == pes[0]["strike"] else None,
        "top_ce": ces[:5],
        "top_pe": pes[:5],
        "source": "NSE India option-chain (jugaad_data NSELive)",
    }


def _exp_match(ed: str, want: str) -> bool:
    a = ed.strip().upper().replace(" ", "")
    b = want.strip().upper().replace(" ", "")
    if a == b:
        return True
    # 18-Aug-2026 vs 18-08-2026
    months = {m: f"{i:02d}" for i, m in enumerate(
        ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}
    def norm(s: str) -> str:
        s = s.replace("-", "")
        for name, num in months.items():
            if name in s:
                s = s.replace(name, num)
                break
        return s
    return norm(a) == norm(b)


def pine_block(data: dict) -> str:
    sup = data["support"]["strike"]
    res = data["resistance"]["strike"]
    sup_oi = data["support"]["oi"]
    res_oi = data["resistance"]["oi"]
    return "\n".join([
        MARK_BEGIN,
        f'// Fetched {data["fetched_at_utc"]} · {data["symbol"]} · expiry {data["expiry"]} · spot {data["spot"]}',
        f'// Source: {data["source"]}',
        f'onlineOiSup = {sup}.0',
        f'onlineOiRes = {res}.0',
        f'onlineOiSupLots = {sup_oi}',
        f'onlineOiResLots = {res_oi}',
        f'onlineOiLabel = "{data["symbol"]} {data["expiry"]}"',
        MARK_END,
    ])


def patch_pine(data: dict) -> None:
    text = PINE.read_text()
    block = pine_block(data)
    if MARK_BEGIN in text and MARK_END in text:
        text = re.sub(
            re.escape(MARK_BEGIN) + r".*?" + re.escape(MARK_END),
            block,
            text,
            count=1,
            flags=re.S,
        )
    else:
        raise SystemExit("Strike_Rate.pine missing ONLINE_OI markers — add the OI block first.")
    PINE.write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", nargs="?", default="NIFTY")
    ap.add_argument("--expiry", default=None, help="e.g. 25-Aug-2026 or 25-08-2026")
    ap.add_argument("--no-pine", action="store_true", help="Only write oi_walls.json")
    args = ap.parse_args()

    data = fetch(args.symbol, args.expiry)
    OUT.write_text(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))
    if not args.no_pine:
        patch_pine(data)
        print(f"Updated {PINE.name}: Support PE {data['support']['strike']} · Resistance CE {data['resistance']['strike']}")


if __name__ == "__main__":
    main()
