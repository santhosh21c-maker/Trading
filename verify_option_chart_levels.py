#!/usr/bin/env python3
"""Verify pre-open option chart logic against NSE FO Daily OHLC.

Locked logic (this option's previous Daily candle):
  Green = C
  Red   = BC = (H + L) / 2
  Red2  = C + (H - L)   # when a second red is present
"""

from __future__ import annotations

from datetime import date

try:
    from jugaad_data.nse import derivatives_df, index_df
except ImportError:
    derivatives_df = index_df = None


CASES = [
    {
        "name": "24150 PE",
        "strike": 24150,
        "opt": "PE",
        "prior": date(2026, 8, 27),
        "green": 79.20,
        "red_bc": 64.30,
    },
    {
        "name": "24250 PE",
        "strike": 24250,
        "opt": "PE",
        "prior": date(2026, 8, 26),
        "green": 69.60,
        "red_bc": 60.50,
        "red_ext": 116.50,
    },
    {
        "name": "24200 PE",
        "strike": 24200,
        "opt": "PE",
        "prior": date(2026, 8, 24),
        "green": 123.30,
        "red_bc": 104.70,
    },
    {
        "name": "24200 CE",
        "strike": 24200,
        "opt": "CE",
        "prior": date(2026, 8, 24),
        "green": 159.55,
        "red_bc": 193.85,
    },
]


def fetch_option(strike: int, opt: str, day: date) -> dict[str, float]:
    if derivatives_df is None:
        raise SystemExit("pip install jugaad-data")
    df = derivatives_df(
        symbol="NIFTY",
        from_date=date(2026, 8, 20),
        to_date=day,
        expiry_date=date(2026, 9, 1),
        instrument_type="OPTIDX",
        option_type=opt,
        strike_price=strike,
    )
    for _, row in df.iterrows():
        d = row["DATE"].date() if hasattr(row["DATE"], "date") else row["DATE"]
        if str(d).startswith(str(day)):
            return {
                "o": float(row["OPEN"]),
                "h": float(row["HIGH"]),
                "l": float(row["LOW"]),
                "c": float(row["CLOSE"]),
            }
    raise RuntimeError(f"No FO row for {strike}{opt} {day}")


def main() -> None:
    print("Corrected pre-open logic: Green=C, Red=(H+L)/2, Red2=C+(H-L)\n")
    print(
        f"{'Contract':12} {'H':>8} {'L':>8} {'C':>8} {'BC':>8} {'Red':>8} {'ΔBC':>7} "
        f"{'Green':>8} {'ΔC':>7} {'C+R':>8}"
    )
    for case in CASES:
        op = fetch_option(case["strike"], case["opt"], case["prior"])
        h, l, c = op["h"], op["l"], op["c"]
        bc = (h + l) / 2
        ext = c + (h - l)
        print(
            f"{case['name']:12} {h:8.2f} {l:8.2f} {c:8.2f} {bc:8.2f} "
            f"{case['red_bc']:8.2f} {bc-case['red_bc']:7.2f} "
            f"{case['green']:8.2f} {c-case['green']:7.2f} {ext:8.2f}"
        )
        if "red_ext" in case:
            print(
                f"{'':12}   upper red {case['red_ext']:.2f} vs C+(H-L)={ext:.2f} "
                f"Δ{ext-case['red_ext']:.2f}"
            )
        pp = (h + l + c) / 3
        tc = 2 * pp - bc
        top, bot = max(tc, bc), min(tc, bc)
        print(
            f"{'':12}   CPR visual top={top:.2f} pivot={pp:.2f} bot={bot:.2f}"
        )
        print()


if __name__ == "__main__":
    main()
