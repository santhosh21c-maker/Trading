#!/usr/bin/env python3
"""
Strike Rate — entries-per-day frequency study across Nifty strikes.

Engines run on INDEX 5m (same idea as Strike_Rate.pine).
Premium paths are synthetic ATM± strikes (Yahoo has no NSE option chain OHLC).
Goal: measure how often chart-track entries fire, and which settings reach ≥2/day.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import yfinance as yf

TP1, TP2, SL = 10.0, 30.0, 18.0
SESSION = ("09:20", "14:45")
MUTE = ("12:15", "13:15")
FLAT = ("15:10", "15:20")


def download_nifty_5m(period: str = "60d") -> pd.DataFrame:
    d = yf.download("^NSEI", period=period, interval="5m", progress=False, auto_adjust=True)
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = [c[0] for c in d.columns]
    d = d.rename(columns=str.title).dropna(subset=["Open", "High", "Low", "Close"])
    if d.index.tz is not None:
        d = d.tz_convert("Asia/Kolkata")
    d = d.between_time("09:15", "15:29")
    rng = (d["High"] - d["Low"]).clip(lower=1e-6)
    d["Volume"] = d["Volume"].fillna(0).replace(0, np.nan).fillna(rng * 1000)
    return d


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def rma(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(alpha=1 / n, adjust=False).mean()


def atr_tr(h, l, c, n=14) -> pd.Series:
    prev = c.shift(1)
    tr = pd.concat([(h - l), (h - prev).abs(), (l - prev).abs()], axis=1).max(axis=1)
    return rma(tr, n)


def adx(h, l, c, n=14) -> pd.Series:
    up = h.diff()
    dn = -l.diff()
    plus_dm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=h.index)
    minus_dm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=h.index)
    tr = atr_tr(h, l, c, 1)
    atr_n = rma(tr, n)
    pdi = 100 * rma(plus_dm, n) / atr_n.replace(0, np.nan)
    mdi = 100 * rma(minus_dm, n) / atr_n.replace(0, np.nan)
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return rma(dx, n)


def supertrend_dir(h, l, c, fac=1.5, length=7) -> pd.Series:
    atr = atr_tr(h, l, c, length)
    mid = (h + l) / 2
    ub = mid + fac * atr
    lb = mid - fac * atr
    fu = ub.copy()
    fl = lb.copy()
    d = pd.Series(1, index=c.index, dtype=int)
    for i in range(1, len(c)):
        fu.iloc[i] = ub.iloc[i] if (ub.iloc[i] < fu.iloc[i - 1] or c.iloc[i - 1] > fu.iloc[i - 1]) else fu.iloc[i - 1]
        fl.iloc[i] = lb.iloc[i] if (lb.iloc[i] > fl.iloc[i - 1] or c.iloc[i - 1] < fl.iloc[i - 1]) else fl.iloc[i - 1]
        if c.iloc[i] > fu.iloc[i - 1]:
            d.iloc[i] = 1
        elif c.iloc[i] < fl.iloc[i - 1]:
            d.iloc[i] = -1
        else:
            d.iloc[i] = d.iloc[i - 1]
    return d


def in_session(idx: pd.DatetimeIndex, start: str, end: str) -> np.ndarray:
    from datetime import time as dtime

    sh, sm = map(int, start.split(":"))
    eh, em = map(int, end.split(":"))
    a, b = dtime(sh, sm), dtime(eh, em)
    return np.array([a <= t.time() <= b for t in idx])


def build_premium(spot: pd.DataFrame, side: str, strike_off: int) -> pd.DataFrame:
    """Synthetic premium for ATM+strike_off (points). CE ITM if off<0; PE ITM if off>0."""
    c = spot["Close"]
    day = c.index.date
    day_open = c.groupby(day).transform("first")
    d_atr = atr_tr(spot["High"], spot["Low"], spot["Close"], 14).groupby(day).transform("first")
    d_atr = d_atr.fillna(atr_tr(spot["High"], spot["Low"], spot["Close"], 14))
    # moneyness scale: ATM ~0.50 delta; ±50 ~0.40/0.60; ±100 ~0.30/0.70
    abs_off = abs(strike_off)
    if side == "CE":
        delta = 0.50 - 0.0010 * strike_off  # +50 OTM → lower delta
    else:
        delta = 0.50 + 0.0010 * strike_off  # +50 ITM for PE
    delta = float(np.clip(delta, 0.25, 0.75))
    base = (0.55 * d_atr * (delta / 0.50)).clip(lower=25, upper=280)
    # intrinsic-ish from strike distance vs spot open
    move = c - day_open
    if side == "CE":
        # strike ≈ day_open + strike_off
        intrinsic = delta * move - 0.15 * max(strike_off, 0)
    else:
        intrinsic = delta * (-move) - 0.15 * max(-strike_off, 0)
    bars = c.groupby(day).cumcount()
    theta = bars * (0.12 + 0.03 * (abs_off / 100.0))
    close = (base + intrinsic - theta).clip(lower=3.0)
    prem = pd.DataFrame(index=spot.index)
    prem["Close"] = close
    prem["Open"] = close.shift(1).fillna(close)
    rng = spot["High"] - spot["Low"]
    if side == "CE":
        prem["High"] = (close + delta * (spot["High"] - c).abs() + 0.1 * rng).clip(lower=prem[["Open", "Close"]].max(axis=1))
        prem["Low"] = (close - delta * (c - spot["Low"]).abs()).clip(upper=prem[["Open", "Close"]].min(axis=1), lower=1.0)
    else:
        prem["High"] = (close + delta * (c - spot["Low"]).abs() + 0.1 * rng).clip(lower=prem[["Open", "Close"]].max(axis=1))
        prem["Low"] = (close - delta * (spot["High"] - c).abs()).clip(upper=prem[["Open", "Close"]].min(axis=1), lower=1.0)
    bad = prem["Low"] > prem["High"]
    prem.loc[bad, "Low"] = prem.loc[bad, ["Open", "Close"]].min(axis=1)
    prem.loc[bad, "High"] = prem.loc[bad, ["Open", "Close"]].max(axis=1)
    prem["Volume"] = spot["Volume"].values
    return prem


@dataclass
class Cfg:
    name: str
    mode: str  # Sniper | Scanner
    cons_n: int  # 1=Any, 2=Two agree
    use_adx: bool
    max_day: int
    mute: bool = True
    hold_to_t1: bool = True


def engine_matrix(spot: pd.DataFrame) -> pd.DataFrame:
    """Compute Strike Rate engines on index bars. Returns bool columns a1..a8 (buy side for CE; flip later)."""
    h, l, c, v = spot["High"], spot["Low"], spot["Close"], spot["Volume"]
    d_atr = atr_tr(h, l, c, 14)
    day = c.index.date
    new_day = pd.Series(day, index=c.index) != pd.Series(day, index=c.index).shift(1)

    # VWAP
    typ = (h + l + c) / 3
    cpv = (typ * v).groupby(day).cumsum()
    cv = v.groupby(day).cumsum().replace(0, np.nan)
    vwap = cpv / cv

    # prior day pivots
    daily = spot.resample("1D").agg({"High": "max", "Low": "min", "Close": "last"})
    pdH = daily["High"].shift(1).reindex(spot.index, method="ffill")
    pdL = daily["Low"].shift(1).reindex(spot.index, method="ffill")
    pdC = daily["Close"].shift(1).reindex(spot.index, method="ffill")
    pP = (pdH + pdL + pdC) / 3
    pB0 = (pdH + pdL) / 2
    pT0 = 2 * pP - pB0
    pTC = pd.concat([pT0, pB0], axis=1).max(axis=1)
    pBC = pd.concat([pT0, pB0], axis=1).min(axis=1)
    pR1 = 2 * pP - pdL
    pS1 = 2 * pP - pdH

    # ORB 30m
    mins = spot.index.map(lambda t: t.hour * 60 + t.minute)
    day_start_min = 9 * 60 + 15
    in_or = (mins - day_start_min) < 30
    orH = pd.Series(np.nan, index=spot.index)
    orL = pd.Series(np.nan, index=spot.index)
    orUp = pd.Series(False, index=spot.index)
    orDn = pd.Series(False, index=spot.index)
    cur_h = cur_l = np.nan
    up = dn = False
    last = None
    for i, ts in enumerate(spot.index):
        d0 = ts.date()
        if d0 != last:
            cur_h = cur_l = np.nan
            up = dn = False
            last = d0
        if in_or[i]:
            cur_h = h.iloc[i] if np.isnan(cur_h) else max(cur_h, h.iloc[i])
            cur_l = l.iloc[i] if np.isnan(cur_l) else min(cur_l, l.iloc[i])
        else:
            if not np.isnan(cur_h) and c.iloc[i] > cur_h:
                up = True
            if not np.isnan(cur_l) and c.iloc[i] < cur_l:
                dn = True
        orH.iloc[i] = cur_h
        orL.iloc[i] = cur_l
        orUp.iloc[i] = up
        orDn.iloc[i] = dn

    dirF = supertrend_dir(h, l, c, 1.5, 7)
    dirS = supertrend_dir(h, l, c, 3.0, 10)
    e9, e21, e50 = ema(c, 9), ema(c, 21), ema(c, 50)
    slUp = (e50 - e50.shift(3)) > 0
    slDn = (e50 - e50.shift(3)) < 0
    xUp = (e9 > e21) & (e9.shift(1) <= e21.shift(1))
    xDn = (e9 < e21) & (e9.shift(1) >= e21.shift(1))
    # bars since cross
    sXU = pd.Series(np.nan, index=c.index)
    sXD = pd.Series(np.nan, index=c.index)
    last_u = last_d = None
    for i in range(len(c)):
        if xUp.iloc[i]:
            last_u = i
        if xDn.iloc[i]:
            last_d = i
        sXU.iloc[i] = i - last_u if last_u is not None else np.nan
        sXD.iloc[i] = i - last_d if last_d is not None else np.nan

    bbD = 2.0 * c.rolling(20).std()
    tr = atr_tr(h, l, c, 1)
    kcR = rma(tr, 20) * 1.5
    sqz = bbD < kcR
    fire = (~sqz) & sqz.shift(1).fillna(False)
    ref = ((h.rolling(20).max() + l.rolling(20).min()) / 2 + sma(c, 20)) / 2
    # linreg proxy: slope * x of (c-ref)
    def linreg0(s, length=20):
        out = pd.Series(np.nan, index=s.index)
        x = np.arange(length)
        x = x - x.mean()
        denom = (x ** 2).sum()
        vals = s.values
        for i in range(length - 1, len(s)):
            y = vals[i - length + 1 : i + 1]
            if np.any(np.isnan(y)):
                continue
            y = y - np.mean(y)
            out.iloc[i] = (x * y).sum() / denom * (length - 1)  # endpoint approx
        return out

    mom = linreg0(c - ref, 20)
    sF = pd.Series(np.nan, index=c.index)
    last_f = None
    for i in range(len(c)):
        if fire.iloc[i]:
            last_f = i
        sF.iloc[i] = i - last_f if last_f is not None else np.nan

    # pivots L/R=5
    lPH = pd.Series(np.nan, index=c.index)
    lPL = pd.Series(np.nan, index=c.index)
    hv, lv = h.values, l.values
    cur_ph = cur_pl = np.nan
    for i in range(5, len(c) - 5):
        if hv[i] == np.nanmax(hv[i - 5 : i + 6]):
            cur_ph = hv[i]
        if lv[i] == np.nanmin(lv[i - 5 : i + 6]):
            cur_pl = lv[i]
        # confirm delayed by 5 like Pine — set at i+5
        if i + 5 < len(c):
            if hv[i] == np.nanmax(hv[i - 5 : i + 6]):
                lPH.iloc[i + 5] = hv[i]
            if lv[i] == np.nanmin(lv[i - 5 : i + 6]):
                lPL.iloc[i + 5] = lv[i]
    lPH = lPH.ffill()
    lPL = lPL.ffill()

    vS = sma(v, 20)
    wid = (h - l) > 1.2 * d_atr
    tTh = ((h - l) > 0) & ((c - l) > 0.66 * (h - l))
    bTh = ((h - l) > 0) & ((h - c) > 0.66 * (h - l))

    xoPTC = (c > pTC) & (c.shift(1) <= pTC.shift(1))
    xoPR1 = (c > pR1) & (c.shift(1) <= pR1.shift(1))
    xuPBC = (c < pBC) & (c.shift(1) >= pBC.shift(1))
    xuPS1 = (c < pS1) & (c.shift(1) >= pS1.shift(1))
    xoVwap = (c > vwap) & (c.shift(1) <= vwap.shift(1))
    xuVwap = (c < vwap) & (c.shift(1) >= vwap.shift(1))
    xoLPH = (c > lPH) & (c.shift(1) <= lPH.shift(1))
    xuLPL = (c < lPL) & (c.shift(1) >= lPL.shift(1))

    a1B = xoPTC | xoPR1 | ((l <= pS1) & (c > pS1) & (c > spot["Open"]))
    a1S = xuPBC | xuPS1 | ((h >= pR1) & (c < pR1) & (c < spot["Open"]))
    a2B = xoVwap & (c > spot["Open"]) & ((c - vwap) >= 0.30 * d_atr)
    a2S = xuVwap & (c < spot["Open"]) & ((vwap - c) >= 0.30 * d_atr)
    a3B = orUp.shift(1).fillna(False) & (l <= orH) & (c > orH) & (c > spot["Open"])
    a3S = orDn.shift(1).fillna(False) & (h >= orL) & (c < orL) & (c < spot["Open"])
    a4B = (dirF == 1) & (dirS == 1) & ((dirF.shift(1) != 1) | (dirS.shift(1) != 1))
    a4S = (dirF == -1) & (dirS == -1) & ((dirF.shift(1) != -1) | (dirS.shift(1) != -1))
    a5B = sXU.notna() & (sXU <= 3) & (e21 > e50) & slUp
    a5S = sXD.notna() & (sXD <= 3) & (e21 < e50) & slDn
    a6B = sF.notna() & (sF <= 3) & (mom > 0) & (mom > mom.shift(1))
    a6S = sF.notna() & (sF <= 3) & (mom < 0) & (mom < mom.shift(1))
    a7B = lPH.notna() & xoLPH
    a7S = lPL.notna() & xuLPL
    a8B = (v > 2.0 * vS) & wid & tTh & (c > spot["Open"])
    a8S = (v > 2.0 * vS) & wid & bTh & (c < spot["Open"])

    out = pd.DataFrame(index=spot.index)
    out["a1B"], out["a1S"] = a1B, a1S
    out["a2B"], out["a2S"] = a2B, a2S
    out["a3B"], out["a3S"] = a3B, a3S
    out["a4B"], out["a4S"] = a4B, a4S
    out["a5B"], out["a5S"] = a5B, a5S
    out["a6B"], out["a6S"] = a6B, a6S
    out["a7B"], out["a7S"] = a7B, a7S
    out["a8B"], out["a8S"] = a8B, a8S
    out["adx"] = adx(h, l, c, 14)
    out["spot"] = c
    return out.fillna(False) if False else out  # keep adx float


def simulate_chart(
    eng: pd.DataFrame,
    prem: pd.DataFrame,
    side: str,
    cfg: Cfg,
) -> pd.DataFrame:
    """Return entries dataframe for chart track (confluence / any)."""
    is_ce = side == "CE"
    on = [True, cfg.mode == "Scanner", True, True, cfg.mode == "Scanner", cfg.mode == "Scanner", cfg.mode == "Scanner", True]
    # pick buy flags for this side
    keys = [f"a{i}{'B' if is_ce else 'S'}" for i in range(1, 9)]
    fires = np.column_stack([eng[k].astype(bool).values for k in keys])

    corr = prem["Close"].rolling(20).corr(eng["spot"])
    sgn = 1.0 if is_ce else -1.0
    sync_ok = (corr * sgn).fillna(0) >= 0.30
    prem_ok = prem["Close"] > prem["Close"].shift(1)
    in_ses = in_session(prem.index, *SESSION)
    in_mute = in_session(prem.index, *MUTE) if cfg.mute else np.zeros(len(prem), dtype=bool)
    in_flat = in_session(prem.index, *FLAT)
    adx_ok = np.ones(len(prem), dtype=bool) if not cfg.use_adx else (eng["adx"].fillna(0).values >= 18.0)
    allow = in_ses & (~in_mute) & sync_ok.fillna(False).values & prem_ok.fillna(False).values & adx_ok

    entries = []
    in_trade = False
    entry_px = stop = rem = realized = 0.0
    booked = False
    day_n = 0
    last_day = None
    mfe = 0.0

    for i in range(len(prem)):
        d0 = prem.index[i].date()
        if d0 != last_day:
            day_n = 0
            last_day = d0

        votes = int(sum(1 for j in range(8) if on[j] and fires[i, j]))
        want_in = votes >= cfg.cons_n

        hi, lo, cl = float(prem["High"].iloc[i]), float(prem["Low"].iloc[i]), float(prem["Close"].iloc[i])

        if in_trade:
            mfe = max(mfe, hi - entry_px)
            out = False
            opx = cl
            why = ""
            if lo <= stop:
                out, opx, why = True, stop, "SL"
            else:
                if (not booked) and hi >= entry_px + TP1:
                    booked = True
                    realized += 0.5 * TP1
                    rem -= 0.5
                    stop = entry_px
                if hi >= entry_px + TP2:
                    realized += rem * TP2
                    rem = 0.0
                    out, opx, why = True, entry_px + TP2, "T2"
                elif in_flat[i]:
                    out, opx, why = True, cl, "EOD"
                elif (not cfg.hold_to_t1 or booked) and votes < cfg.cons_n:
                    out, opx, why = True, cl, "EXIT"
            if out:
                if rem > 0:
                    realized += rem * (opx - entry_px)
                entries[-1].update(
                    {
                        "exit_time": prem.index[i],
                        "pnl": realized,
                        "mfe": mfe,
                        "booked_t1": booked,
                        "why": why,
                    }
                )
                in_trade = False
        else:
            if want_in and allow[i] and (not in_flat[i]) and day_n < cfg.max_day and cl > 0:
                in_trade = True
                entry_px = cl
                stop = cl - SL
                rem = 1.0
                realized = 0.0
                booked = False
                mfe = 0.0
                day_n += 1
                entries.append(
                    {
                        "entry_time": prem.index[i],
                        "day": d0,
                        "side": side,
                        "entry": entry_px,
                        "votes": votes,
                        "cfg": cfg.name,
                    }
                )

    return pd.DataFrame(entries)


def summarize(trades: pd.DataFrame, session_days: int, label: str) -> Dict:
    if trades.empty:
        return {
            "label": label,
            "trades": 0,
            "session_days": session_days,
            "active_days": 0,
            "avg_per_session_day": 0.0,
            "avg_per_active_day": 0.0,
            "pct_days_ge2": 0.0,
            "pct_days_ge1": 0.0,
            "median_active": 0.0,
            "net": 0.0,
            "t1_pct": 0.0,
        }
    by = trades.groupby("day").size()
    active = len(by)
    ge2 = (by >= 2).mean() * 100
    ge1 = (by >= 1).mean() * 100 if False else (len(by) / max(session_days, 1)) * 100
    # % of ALL session days with ≥2
    days_ge2 = int((by >= 2).sum())
    return {
        "label": label,
        "trades": int(len(trades)),
        "session_days": session_days,
        "active_days": active,
        "avg_per_session_day": round(len(trades) / max(session_days, 1), 3),
        "avg_per_active_day": round(float(by.mean()), 3),
        "pct_session_days_ge2": round(100.0 * days_ge2 / max(session_days, 1), 1),
        "pct_session_days_ge1": round(100.0 * active / max(session_days, 1), 1),
        "median_active": round(float(by.median()), 2),
        "net": round(float(trades["pnl"].fillna(0).sum()), 1) if "pnl" in trades else 0.0,
        "t1_pct": round(100.0 * trades["booked_t1"].fillna(False).mean(), 1) if "booked_t1" in trades else 0.0,
    }


def main():
    print("Downloading Nifty 5m…")
    spot = download_nifty_5m("60d")
    print(f"Bars: {len(spot)}  days: {spot.index.normalize().nunique()}  "
          f"{spot.index[0].date()} → {spot.index[-1].date()}")
    session_days = int(spot.index.normalize().nunique())
    eng = engine_matrix(spot)

    # Strikes relative to rolling ATM (rounded 50)
    atm0 = int(round(float(spot["Close"].iloc[-1]) / 50) * 50)
    offsets = [-100, -50, 0, 50, 100]
    strikes = [atm0 + o for o in offsets]
    print(f"ATM≈{atm0}  testing strikes: {strikes}")

    cfgs = [
        Cfg("Sniper·TwoAgree·ADX·max2 (v1.1 default)", "Sniper", 2, True, 2),
        Cfg("Sniper·TwoAgree·noADX·max3", "Sniper", 2, False, 3),
        Cfg("Sniper·Any·ADX·max3", "Sniper", 1, True, 3),
        Cfg("Sniper·Any·noADX·max3", "Sniper", 1, False, 3),
        Cfg("Scanner·TwoAgree·ADX·max3", "Scanner", 2, True, 3),
        Cfg("Scanner·Any·noADX·max3  ★ target≥2/day", "Scanner", 1, False, 3),
        Cfg("Scanner·Any·noADX·max4", "Scanner", 1, False, 4),
        Cfg("Scanner·Any·noMute·max4", "Scanner", 1, False, 4, mute=False),
    ]

    rows = []
    strike_rows = []
    best_for_2 = None

    for cfg in cfgs:
        all_tr = []
        for side in ("CE", "PE"):
            for off in offsets:
                prem = build_premium(spot, side, off)
                tr = simulate_chart(eng, prem, side, cfg)
                if not tr.empty:
                    tr["strike"] = atm0 + off
                    tr["moneyness"] = (
                        "ATM" if off == 0 else ("ITM" if (side == "CE" and off < 0) or (side == "PE" and off > 0) else "OTM")
                    )
                    all_tr.append(tr)
                    s = summarize(tr, session_days, f"{cfg.name}|{side}|{atm0+off}")
                    s.update({"cfg": cfg.name, "side": side, "strike": atm0 + off, "off": off})
                    strike_rows.append(s)
        if all_tr:
            cat = pd.concat(all_tr, ignore_index=True)
        else:
            cat = pd.DataFrame()
        # Per-chart average: mean across the 10 contracts of avg_per_session_day
        if strike_rows:
            subset = [r for r in strike_rows if r["cfg"] == cfg.name]
            avg_sess = float(np.mean([r["avg_per_session_day"] for r in subset])) if subset else 0.0
            avg_act = float(np.mean([r["avg_per_active_day"] for r in subset])) if subset else 0.0
            pct_ge2 = float(np.mean([r["pct_session_days_ge2"] for r in subset])) if subset else 0.0
            # CE+PE same day combined on ATM only
            atm_ce = cat[(cat.get("strike") == atm0) & (cat.get("side") == "CE")] if not cat.empty else cat
            atm_pe = cat[(cat.get("strike") == atm0) & (cat.get("side") == "PE")] if not cat.empty else cat
            # single-chart ATM CE frequency (what user sees on one chart)
            atm_ce_s = summarize(
                cat[(cat["strike"] == atm0) & (cat["side"] == "CE")] if not cat.empty else pd.DataFrame(),
                session_days,
                "ATM CE",
            )
            atm_pe_s = summarize(
                cat[(cat["strike"] == atm0) & (cat["side"] == "PE")] if not cat.empty else pd.DataFrame(),
                session_days,
                "ATM PE",
            )
        else:
            avg_sess = avg_act = pct_ge2 = 0.0
            atm_ce_s = atm_pe_s = summarize(pd.DataFrame(), session_days, "x")

        row = {
            "cfg": cfg.name,
            "mode": cfg.mode,
            "cons_n": cfg.cons_n,
            "adx": cfg.use_adx,
            "max_day": cfg.max_day,
            "mute": cfg.mute,
            "avg_entries_per_session_day_per_chart": round(avg_sess, 3),
            "avg_on_active_days": round(avg_act, 3),
            "pct_session_days_with_ge2": round(pct_ge2, 1),
            "ATM_CE_per_session_day": atm_ce_s["avg_per_session_day"],
            "ATM_CE_per_active_day": atm_ce_s["avg_per_active_day"],
            "ATM_CE_pct_days_ge2": atm_ce_s["pct_session_days_ge2"],
            "ATM_PE_per_session_day": atm_pe_s["avg_per_session_day"],
            "ATM_PE_per_active_day": atm_pe_s["avg_per_active_day"],
            "ATM_PE_pct_days_ge2": atm_pe_s["pct_session_days_ge2"],
            "ATM_CE_t1_pct": atm_ce_s["t1_pct"],
            "ATM_PE_t1_pct": atm_pe_s["t1_pct"],
            "ATM_CE_net": atm_ce_s["net"],
            "ATM_PE_net": atm_pe_s["net"],
        }
        rows.append(row)
        print(f"\n=== {cfg.name} ===")
        print(
            f"  Per chart avg: {avg_sess:.2f}/session-day · {avg_act:.2f}/active-day · "
            f"{pct_ge2:.0f}% of days have ≥2"
        )
        print(
            f"  ATM CE: {atm_ce_s['avg_per_session_day']:.2f}/day "
            f"({atm_ce_s['avg_per_active_day']:.2f} on active) · "
            f"≥2 on {atm_ce_s['pct_session_days_ge2']}% days · T1 {atm_ce_s['t1_pct']}%"
        )
        print(
            f"  ATM PE: {atm_pe_s['avg_per_session_day']:.2f}/day "
            f"({atm_pe_s['avg_per_active_day']:.2f} on active) · "
            f"≥2 on {atm_pe_s['pct_session_days_ge2']}% days · T1 {atm_pe_s['t1_pct']}%"
        )

    summary = pd.DataFrame(rows)
    detail = pd.DataFrame(strike_rows)
    summary.to_csv("/workspace/STRIKE_RATE_FREQ_SUMMARY.csv", index=False)
    detail.to_csv("/workspace/STRIKE_RATE_FREQ_BY_STRIKE.csv", index=False)

    # Prefer configs that hit ≥2 per SESSION day on ATM (user goal), not just active-day
    pick = None
    for r in rows:
        if r["ATM_CE_per_session_day"] >= 2.0 or r["ATM_PE_per_session_day"] >= 2.0:
            pick = r
            break
    if pick is None:
        for r in rows:
            if r["avg_on_active_days"] >= 2:
                pick = r
                break
    if pick is None:
        pick = max(rows, key=lambda r: r["avg_entries_per_session_day_per_chart"])

    md = []
    md.append("# Strike Rate — entries per day (multi-strike)")
    md.append("")
    md.append(f"**Data:** Nifty 5m Yahoo `^NSEI` · {spot.index[0].date()} → {spot.index[-1].date()} · **{session_days} session days**")
    md.append(f"**Strikes tested:** {strikes} (ATM≈{atm0} ±50/100) · CE & PE synthetic premiums")
    md.append("**Note:** Free feeds lack real NSE option OHLC; premium paths are synthetic. Frequency is driven mainly by **index engines + filters**, so strike differences are modest.")
    md.append("")
    md.append("## Headline — do we get ≥2 entries/day?")
    md.append("")
    md.append("| Config | Avg / session-day (per chart) | Avg / active day | % days with ≥2 | ATM CE /day | ATM PE /day |")
    md.append("|--------|------------------------------:|-----------------:|---------------:|------------:|------------:|")
    for r in rows:
        md.append(
            f"| {r['cfg']} | {r['avg_entries_per_session_day_per_chart']:.2f} | "
            f"{r['avg_on_active_days']:.2f} | {r['pct_session_days_with_ge2']:.0f}% | "
            f"{r['ATM_CE_per_session_day']:.2f} | {r['ATM_PE_per_session_day']:.2f} |"
        )
    md.append("")
    md.append(f"**Best for frequency:** `{pick['cfg']}`")
    md.append("")
    md.append("### Practical reading")
    md.append("")
    md.append("- **v1.1 default (Sniper · Two agree · ADX · max2)** stays near **~1 entry on a signal day**, and many days are flat — that is by design.")
    md.append("- To push toward **≥2 entries/day**, use **Scanner + Any engine**, raise **Max chart entries/day to 3–4**, and consider turning **ADX off** (and optionally midday mute).")
    md.append("- More entries ≠ better PnL. Prior SL18 lab: looser gates cut expectancy. Trade the frequency setting small.")
    md.append("")
    md.append("## By strike (recommended frequency config)")
    md.append("")
    md.append(f"Config: **{pick['cfg']}**")
    md.append("")
    md.append("| Side | Strike | Moneyness | Trades | /session-day | /active-day | % days ≥2 | T1% | Net |")
    md.append("|------|-------:|-----------|-------:|-------------:|------------:|----------:|----:|----:|")
    for r in sorted([x for x in strike_rows if x["cfg"] == pick["cfg"]], key=lambda z: (z["side"], z["strike"])):
        m = "ATM" if r["off"] == 0 else ("ITM" if (r["side"] == "CE" and r["off"] < 0) or (r["side"] == "PE" and r["off"] > 0) else "OTM")
        md.append(
            f"| {r['side']} | {r['strike']} | {m} | {r['trades']} | {r['avg_per_session_day']:.2f} | "
            f"{r['avg_per_active_day']:.2f} | {r['pct_session_days_ge2']:.0f}% | {r['t1_pct']:.0f}% | {r['net']:.1f} |"
        )
    md.append("")
    md.append("Files: `STRIKE_RATE_FREQ_SUMMARY.csv`, `STRIKE_RATE_FREQ_BY_STRIKE.csv`, `backtest_strike_rate_frequency.py`")
    path = "/workspace/STRIKE_RATE_FREQ_REPORT.md"
    open(path, "w").write("\n".join(md))
    print("\nWrote", path)
    print(summary.to_string(index=False))
    return pick


if __name__ == "__main__":
    main()
