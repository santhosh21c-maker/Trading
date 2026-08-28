#!/usr/bin/env python3
"""Verify TBT option-chart horizontals against prior-day OHLC only (pre-open)."""

from __future__ import annotations

from datetime import date

try:
    from jugaad_data.nse import derivatives_df, index_df
except ImportError:
    derivatives_df = index_df = None


def cpr_bc(h: float, l: float) -> float:
    return (h + l) / 2


def camarilla(c: float, h: float, l: float) -> dict[str, float]:
    r = h - l
    return {
        "CR4": c + r * 1.1 / 2,
        "CR3": c + r * 1.1 / 4,
        "CR2": c + r * 1.1 / 6,
        "CR1": c + r * 1.1 / 12,
        "CS1": c - r * 1.1 / 12,
        "CS2": c - r * 1.1 / 6,
        "CS3": c - r * 1.1 / 4,
        "CS4": c - r * 1.1 / 2,
    }


# Screenshot labels vs expected prior session for that contract
CASES = [
    {
        "name": "24150 PE (chart ~28 Aug)",
        "strike": 24150,
        "opt": "PE",
        "prior": date(2026, 8, 27),
        "green": 79.20,
        "red_bc": 64.30,
    },
    {
        "name": "24250 PE (chart 27 Aug open)",
        "strike": 24250,
        "opt": "PE",
        "prior": date(2026, 8, 26),
        "green": 69.60,
        "red_bc": 60.50,
        "red_ext": 116.50,
    },
    {
        "name": "24200 PE (green~123 / red~104.7)",
        "strike": 24200,
        "opt": "PE",
        "prior": date(2026, 8, 24),
        "green": 123.30,
        "red_bc": 104.70,
    },
    {
        "name": "24200 CE (Px shot)",
        "strike": 24200,
        "opt": "CE",
        "prior": date(2026, 8, 24),
        "green": 159.55,
        "red_bc": 193.85,
    },
]


def fetch_option(strike: int, opt: str, day: date) -> dict[str, float]:
    if derivatives_df is None:
        raise SystemExit("Install jugaad-data: pip install jugaad-data")
    df = derivatives_df(
        symbol="NIFTY",
        from_date=day,
        to_date=day,
        expiry_date=date(2026, 9, 1),
        instrument_type="OPTIDX",
        option_type=opt,
        strike_price=strike,
    )
    if df is None or len(df) == 0:
        # jugaad sometimes needs a range
        df = derivatives_df(
            symbol="NIFTY",
            from_date=date(2026, 8, 20),
            to_date=day,
            expiry_date=date(2026, 9, 1),
            instrument_type="OPTIDX",
            option_type=opt,
            strike_price=strike,
        )
        df = df[df["DATE"].astype(str).str.startswith(str(day))]
    row = df.iloc[0]
    return {
        "o": float(row["OPEN"]),
        "h": float(row["HIGH"]),
        "l": float(row["LOW"]),
        "c": float(row["CLOSE"]),
    }


def fetch_spot(day: date) -> dict[str, float]:
    if index_df is None:
        raise SystemExit("Install jugaad-data: pip install jugaad-data")
    df = index_df(symbol="NIFTY 50", from_date=day, to_date=day)
    if len(df) == 0:
        df = index_df(symbol="NIFTY 50", from_date=date(2026, 8, 20), to_date=day)
        df = df[df["HistoricalDate"].astype(str).str.startswith(str(day))]
    row = df.iloc[0]
    return {
        "o": float(row["OPEN"]),
        "h": float(row["HIGH"]),
        "l": float(row["LOW"]),
        "c": float(row["CLOSE"]),
    }


def main() -> None:
    print("Pre-open check: prior-day OPTION Daily OHLC (exchange) vs chart lines\n")
    print(
        f"{'Case':32} {'H':>8} {'L':>8} {'C':>8} {'BC':>8} {'Red':>8} {'ΔR':>6} "
        f"{'Green':>8} {'ΔG':>6}"
    )
    for case in CASES:
        op = fetch_option(case["strike"], case["opt"], case["prior"])
        sp = fetch_spot(case["prior"])
        pdc = op["c"]
        bc = cpr_bc(op["h"], op["l"])
        g, r = case["green"], case["red_bc"]
        print(
            f"{case['name']:32} {op['h']:8.2f} {op['l']:8.2f} {pdc:8.2f} "
            f"{bc:8.2f} {r:8.2f} {bc-r:6.2f} {g:8.2f} {pdc-g:6.2f}"
        )
        if "red_ext" in case:
            ext = pdc + (op["h"] - op["l"])
            print(
                f"{'':32}   Claim3 C+(H-L)={ext:.2f} vs upper red {case['red_ext']} "
                f"Δ{abs(ext-case['red_ext']):.2f}"
            )
        # Spot traded-low correction note for 27 Aug archive L==C auction
        print(
            f"{'':32}   spot archive C={sp['c']:.2f} L={sp['l']:.2f} "
            f"(if L==C, low may be auction; spot CPR ≠ premium lines)"
        )
        print()


if __name__ == "__main__":
    main()
