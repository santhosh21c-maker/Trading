#!/usr/bin/env python3
"""
Backtest Options Engines Lab v1.0 on synthetic ATM CE/PE premiums
derived from Nifty / BankNifty / Sensex 5-minute index data.

Yahoo Finance does not supply NSE option-chain OHLC, so premiums are
modeled as ATM delta≈0.5 tracks with mild theta — suitable for comparing
engines under the same TP1=10 / TP2=20 / TP3=35 / SL=12 rules as the Pine script.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import yfinance as yf

# ── risk defaults (match Pine) ──────────────────────────────────────────────
TP1, TP2, TP3 = 10.0, 20.0, 35.0
SL_PTS = 12.0
COOLDOWN = 5
MAX_DAY = 6
ORB_MINS = 15
SWING = 5
EMA_F, EMA_M, EMA_S = 9, 21, 50
ADX_MIN = 18.0
USE_SESS = True
USE_LATE = True
USE_CHOP = True
USE_SYNC = True

SYMBOLS = {
    "Nifty": "^NSEI",
    "BankNifty": "^NSEBANK",
    "Sensex": "^BSESN",
}


def download_5m(ticker: str) -> pd.DataFrame:
    d = yf.download(ticker, period="60d", interval="5m", progress=False, auto_adjust=True)
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = [c[0] for c in d.columns]
    d = d.rename(columns=str.title)
    d = d.dropna(subset=["Open", "High", "Low", "Close"])
    # IST session only
    if d.index.tz is not None:
        d = d.tz_convert("Asia/Kolkata")
    d = d.between_time("09:15", "15:29")
    d["Volume"] = d["Volume"].fillna(0).replace(0, np.nan)
    # index volume often 0 — fill with range proxy so E11 can fire
    rng = (d["High"] - d["Low"]).clip(lower=1e-6)
    d["Volume"] = d["Volume"].fillna(rng * 1000)
    return d


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    prev = df["Close"].shift(1)
    tr = pd.concat([
        df["High"] - df["Low"],
        (df["High"] - prev).abs(),
        (df["Low"] - prev).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0)
    dn = -d.clip(upper=0)
    au = up.ewm(alpha=1 / n, adjust=False).mean()
    ad = dn.ewm(alpha=1 / n, adjust=False).mean()
    rs = au / ad.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd_hist(close: pd.Series) -> pd.Series:
    ef, es = ema(close, 12), ema(close, 26)
    line = ef - es
    sig = ema(line, 9)
    return line - sig


def dmi_adx(df: pd.DataFrame, n: int = 14) -> pd.Series:
    up = df["High"].diff()
    dn = -df["Low"].diff()
    plus_dm = np.where((up > dn) & (up > 0), up, 0.0)
    minus_dm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = atr(df, 1)
    atr_n = tr.rolling(n).mean()
    pdi = 100 * pd.Series(plus_dm, index=df.index).rolling(n).mean() / atr_n
    mdi = 100 * pd.Series(minus_dm, index=df.index).rolling(n).mean() / atr_n
    dx = (100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan))
    return dx.rolling(n).mean()


def supertrend(df: pd.DataFrame, period: int = 10, mult: float = 2.0) -> Tuple[pd.Series, pd.Series]:
    a = atr(df, period).bfill()
    hl2 = (df["High"] + df["Low"]) / 2.0
    basic_ub = hl2 + mult * a
    basic_lb = hl2 - mult * a
    final_ub = basic_ub.copy()
    final_lb = basic_lb.copy()
    for i in range(1, len(df)):
        final_ub.iloc[i] = (
            basic_ub.iloc[i]
            if basic_ub.iloc[i] < final_ub.iloc[i - 1] or df["Close"].iloc[i - 1] > final_ub.iloc[i - 1]
            else final_ub.iloc[i - 1]
        )
        final_lb.iloc[i] = (
            basic_lb.iloc[i]
            if basic_lb.iloc[i] > final_lb.iloc[i - 1] or df["Close"].iloc[i - 1] < final_lb.iloc[i - 1]
            else final_lb.iloc[i - 1]
        )
    st = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=float)
    st.iloc[0] = final_ub.iloc[0]
    direction.iloc[0] = 1  # bearish start
    for i in range(1, len(df)):
        if st.iloc[i - 1] == final_ub.iloc[i - 1]:
            direction.iloc[i] = -1 if df["Close"].iloc[i] > final_ub.iloc[i] else 1
        else:
            direction.iloc[i] = 1 if df["Close"].iloc[i] < final_lb.iloc[i] else -1
        st.iloc[i] = final_lb.iloc[i] if direction.iloc[i] == -1 else final_ub.iloc[i]
    return st, direction


def pivots(series: pd.Series, left: int, right: int, mode: str) -> pd.Series:
    out = pd.Series(index=series.index, dtype=float)
    vals = series.values
    n = len(vals)
    for i in range(left, n - right):
        w = vals[i - left : i + right + 1]
        if mode == "high" and vals[i] == np.nanmax(w) and np.sum(w == vals[i]) == 1:
            out.iloc[i + right] = vals[i]  # confirm at i+right like Pine
        if mode == "low" and vals[i] == np.nanmin(w) and np.sum(w == vals[i]) == 1:
            out.iloc[i + right] = vals[i]
    # Pine pivothigh confirms after `right` bars; value appears at bar i+right referencing pivot at i
    # Rebuild properly:
    out[:] = np.nan
    for i in range(left, n - right):
        center = i
        window = vals[center - left : center + right + 1]
        if mode == "high" and vals[center] >= np.nanmax(window):
            out.iloc[center + right] = vals[center]
        if mode == "low" and vals[center] <= np.nanmin(window):
            out.iloc[center + right] = vals[center]
    return out


def session_mask(idx: pd.DatetimeIndex, start: str, end: str) -> np.ndarray:
    t = idx.time
    sh, sm = map(int, start.split(":"))
    eh, em = map(int, end.split(":"))
    from datetime import time as dtime
    a, b = dtime(sh, sm), dtime(eh, em)
    return np.array([(a <= x <= b) for x in t])


def build_synthetic_option(df: pd.DataFrame, side: str) -> pd.DataFrame:
    """ATM-ish premium: delta 0.5 track + mild theta. Typical weekly ATM start ~120."""
    spot = df["Close"]
    day = spot.index.date
    # day open spot
    day_open = spot.groupby(day).transform("first")
    daily_atr = atr(df, 14).groupby(day).transform("first").fillna(atr(df, 14))
    base = (0.55 * daily_atr).clip(lower=40, upper=250)  # starting ATM premium scale
    # path
    move = spot - day_open
    if side == "CE":
        intrinsic_proxy = 0.50 * move
    else:
        intrinsic_proxy = 0.50 * (-move)
    # bars from open for theta
    bars_in_day = spot.groupby(day).cumcount()
    theta = bars_in_day * 0.15  # ~11 pts decay over ~75 five-min bars
    prem_close = (base + intrinsic_proxy - theta).clip(lower=5.0)
    # OHLC envelope from spot range
    spot_rng = df["High"] - df["Low"]
    prem = pd.DataFrame(index=df.index)
    prem["Close"] = prem_close
    prem["Open"] = prem_close.shift(1).fillna(prem_close)
    # wicks from spot micro-moves
    delta_hi = 0.50 * (df["High"] - spot)
    delta_lo = 0.50 * (spot - df["Low"])
    if side == "CE":
        prem["High"] = (prem["Close"] + delta_hi.abs() + 0.2 * spot_rng * 0.5).clip(lower=prem[["Open", "Close"]].max(axis=1))
        prem["Low"] = (prem["Close"] - delta_lo.abs()).clip(upper=prem[["Open", "Close"]].min(axis=1), lower=1.0)
    else:
        prem["High"] = (prem["Close"] + delta_lo.abs() + 0.2 * spot_rng * 0.5).clip(lower=prem[["Open", "Close"]].max(axis=1))
        prem["Low"] = (prem["Close"] - delta_hi.abs()).clip(upper=prem[["Open", "Close"]].min(axis=1), lower=1.0)
    # fix any Low>High
    bad = prem["Low"] > prem["High"]
    prem.loc[bad, "Low"] = prem.loc[bad, ["Open", "Close"]].min(axis=1)
    prem.loc[bad, "High"] = prem.loc[bad, ["Open", "Close"]].max(axis=1)
    prem["Volume"] = df["Volume"].values
    prem["Spot"] = spot.values
    return prem


def prepare(df: pd.DataFrame, und: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["emaF"] = ema(x["Close"], EMA_F)
    x["emaM"] = ema(x["Close"], EMA_M)
    x["emaS"] = ema(x["Close"], EMA_S)
    # VWAP per day
    typ = (x["High"] + x["Low"] + x["Close"]) / 3
    day = x.index.date
    cum_pv = (typ * x["Volume"]).groupby(day).cumsum()
    cum_v = x["Volume"].groupby(day).cumsum().replace(0, np.nan)
    x["vwap"] = cum_pv / cum_v
    x["atr"] = atr(x, 14)
    x["atrAvg"] = sma(x["atr"], 20)
    x["rsi"] = rsi(x["Close"], 14)
    x["macdh"] = macd_hist(x["Close"])
    x["adx"] = dmi_adx(x, 14)
    st, direction = supertrend(x, 10, 2.0)
    x["st"] = st
    x["stDir"] = direction
    x["volMa"] = sma(x["Volume"], 20)
    ph = pivots(x["High"], SWING, SWING, "high")
    pl = pivots(x["Low"], SWING, SWING, "low")
    x["ph"] = ph
    x["pl"] = pl
    # last swing high/low forward-filled
    x["lastSH"] = ph.ffill()
    x["lastSL"] = pl.ffill()
    # prev day H/L of premium
    daily = x.resample("1D").agg({"High": "max", "Low": "min"})
    x["pdH"] = daily["High"].shift(1).reindex(x.index, method="ffill")
    x["pdL"] = daily["Low"].shift(1).reindex(x.index, method="ffill")
    # ORB
    x["or_window"] = session_mask(x.index, "09:15", f"{9 + (15 + ORB_MINS) // 60:02d}:{(15 + ORB_MINS) % 60:02d}")
    or_hi = pd.Series(np.nan, index=x.index)
    or_lo = pd.Series(np.nan, index=x.index)
    cur_h = cur_l = np.nan
    last_day = None
    for i, ts in enumerate(x.index):
        d0 = ts.date()
        if d0 != last_day:
            cur_h = cur_l = np.nan
            last_day = d0
        if x["or_window"].iloc[i]:
            cur_h = x["High"].iloc[i] if np.isnan(cur_h) else max(cur_h, x["High"].iloc[i])
            cur_l = x["Low"].iloc[i] if np.isnan(cur_l) else min(cur_l, x["Low"].iloc[i])
        or_hi.iloc[i] = cur_h
        or_lo.iloc[i] = cur_l
    x["orHi"] = or_hi
    x["orLo"] = or_lo
    # CPR from prior day
    ohlc_d = x.resample("1D").agg({"High": "max", "Low": "min", "Close": "last"})
    p = (ohlc_d["High"] + ohlc_d["Low"] + ohlc_d["Close"]) / 3
    bc = (ohlc_d["High"] + ohlc_d["Low"]) / 2
    tc = 2 * p - bc
    top = pd.concat([tc, bc], axis=1).max(axis=1).shift(1)
    bot = pd.concat([tc, bc], axis=1).min(axis=1).shift(1)
    x["cprTop"] = top.reindex(x.index, method="ffill")
    x["cprBot"] = bot.reindex(x.index, method="ffill")
    x["donHi"] = x["High"].rolling(SWING).max().shift(1)
    x["donLo"] = x["Low"].rolling(SWING).min().shift(1)
    mid = sma(x["Close"], 20)
    std = x["Close"].rolling(20).std()
    x["bbU"] = mid + 2 * std
    x["bbL"] = mid - 2 * std
    x["basis"] = mid
    bbw = (x["bbU"] - x["bbL"]) / mid.replace(0, np.nan) * 100
    x["squeeze"] = bbw < sma(bbw, 50) * 0.75
    # sessions / filters
    x["sessOk"] = session_mask(x.index, "09:20", "11:15") | session_mask(x.index, "13:15", "15:05")
    x["lateBlk"] = session_mask(x.index, "15:00", "15:30")
    x["chopOk"] = x["adx"].fillna(0) >= ADX_MIN
    x["filtersOk"] = ((x["sessOk"] if USE_SESS else True) & (~x["lateBlk"] if USE_LATE else True) & (x["chopOk"] if USE_CHOP else True))
    # underlying bias on same bars
    u = und.reindex(x.index, method="ffill")
    uef, ues = ema(u["Close"], 9), ema(u["Close"], 21)
    x["undBull"] = uef > ues
    x["undBear"] = uef < ues
    # candle patterns
    x["bullEng"] = (x["Close"] > x["Open"]) & (x["Close"].shift(1) < x["Open"].shift(1)) & (x["Close"] >= x["Open"].shift(1)) & (x["Open"] <= x["Close"].shift(1))
    x["bearEng"] = (x["Close"] < x["Open"]) & (x["Close"].shift(1) > x["Open"].shift(1)) & (x["Close"] <= x["Open"].shift(1)) & (x["Open"] >= x["Close"].shift(1))
    x["volOk"] = x["Volume"] > x["volMa"] * 1.2
    rng = (x["High"] - x["Low"]).replace(0, np.nan)
    lo_w = (x[["Open", "Close"]].min(axis=1) - x["Low"]) / rng
    up_w = (x["High"] - x[["Open", "Close"]].max(axis=1)) / rng
    x["bullSweep"] = (lo_w >= 0.55) & (x["Close"] > x["Open"]) & (x["Close"] > x["Close"].shift(1))
    x["bearSweep"] = (up_w >= 0.55) & (x["Close"] < x["Open"]) & (x["Close"] < x["Close"].shift(1))
    x["inside"] = (x["High"] < x["High"].shift(1)) & (x["Low"] > x["Low"].shift(1))
    x["motherHi"] = x["High"].shift(1)
    x["motherLo"] = x["Low"].shift(1)
    step = np.where(x["Close"] >= 100, 10.0, np.where(x["Close"] >= 40, 5.0, 2.5))
    x["rndBelow"] = np.floor(x["Close"].values / step) * step
    x["rndAbove"] = x["rndBelow"] + step
    x["emaStackUp"] = (x["emaF"] > x["emaM"]) & (x["emaM"] > x["emaS"]) & (x["emaF"] > x["emaF"].shift(1))
    x["emaStackDn"] = (x["emaF"] < x["emaM"]) & (x["emaM"] < x["emaS"]) & (x["emaF"] < x["emaF"].shift(1))
    return x


def signals(x: pd.DataFrame, engine: str) -> Tuple[pd.Series, pd.Series]:
    c, o, h, l = x["Close"], x["Open"], x["High"], x["Low"]
    buy = pd.Series(False, index=x.index)
    sell = pd.Series(False, index=x.index)
    if engine == "E1 Swing Structure":
        buy = c.notna() & x["lastSH"].notna() & (c > x["lastSH"]) & (c > o)
        sell = x["lastSL"].notna() & (c < x["lastSL"])
    elif engine == "E2 Opening Range Breakout":
        buy = x["orHi"].notna() & (~x["or_window"]) & (c > x["orHi"]) & (c.shift(1) <= x["orHi"])
        sell = x["orLo"].notna() & ((c < x["orLo"]) | (c < x["vwap"]))
    elif engine == "E3 VWAP Reclaim":
        buy = (c > x["vwap"]) & (c.shift(1) <= x["vwap"]) & (c > o)
        sell = (c < x["vwap"]) & (c.shift(1) >= x["vwap"])
    elif engine == "E4 Prev Day High/Low Break":
        buy = x["pdH"].notna() & (c > x["pdH"]) & (c.shift(1) <= x["pdH"])
        sell = x["pdL"].notna() & (c < x["pdL"])
    elif engine == "E5 Pullback Continuation":
        buy = x["emaStackUp"] & (l <= x["emaF"]) & (c > x["emaF"]) & (c > o)
        sell = c < x["emaM"]
    elif engine == "E6 EMA Stack Momentum":
        buy = x["emaStackUp"] & (~x["emaStackUp"].shift(1).fillna(False))
        sell = x["emaStackDn"]
    elif engine == "E7 ATR Expansion Impulse":
        buy = (x["atr"] > x["atrAvg"]) & (c > o) & ((c - o) > x["atr"] * 0.6) & (c > c.shift(1))
        sell = (x["atr"] < x["atrAvg"]) | ((c < o) & ((o - c) > x["atr"] * 0.5))
    elif engine == "E8 RSI Regime":
        buy = (x["rsi"] > 50) & (x["rsi"].shift(1) <= 50) & (c > x["emaF"])
        sell = (x["rsi"] < 50) & (x["rsi"].shift(1) >= 50)
    elif engine == "E9 MACD Histogram":
        buy = (x["macdh"] > 0) & (x["macdh"].shift(1) <= 0)
        sell = (x["macdh"] < 0) & (x["macdh"].shift(1) >= 0)
    elif engine == "E10 Supertrend":
        buy = (x["stDir"] == -1) & (x["stDir"].shift(1) == 1)
        sell = (x["stDir"] == 1) & (x["stDir"].shift(1) == -1)
    elif engine == "E11 Engulf + Volume":
        buy = x["bullEng"] & x["volOk"]
        sell = x["bearEng"]
    elif engine == "E12 Rejection Wick Sweep":
        buy = x["bullSweep"]
        sell = x["bearSweep"]
    elif engine == "E13 Inside Bar Breakout":
        buy = x["inside"].shift(1).fillna(False) & (c > x["motherHi"]) & (c > o)
        sell = x["inside"].shift(1).fillna(False) & (c < x["motherLo"])
    elif engine == "E14 Round Premium Levels":
        buy = (l <= x["rndBelow"]) & (c > x["rndBelow"]) & (c > o)
        sell = (h >= x["rndAbove"]) & (c < x["rndAbove"])
    elif engine == "E15 Option CPR / Pivot":
        buy = (c > x["cprTop"]) & (c.shift(1) <= x["cprTop"])
        sell = c < x["cprBot"]
    elif engine == "E16 Donchian Channel Break":
        buy = (c > x["donHi"]) & (c > o)
        sell = c < x["donLo"]
    elif engine == "E21 Bollinger Squeeze Break":
        buy = x["squeeze"].shift(1).fillna(False) & (~x["squeeze"]) & (c > x["bbU"])
        sell = c < x["basis"]
    return buy.fillna(False), sell.fillna(False)


@dataclass
class Trade:
    engine: str
    symbol: str
    side: str
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    entry: float
    exit: float
    pnl: float
    reason: str
    hit_tp1: bool
    hit_tp2: bool
    hit_tp3: bool


def run_engine(x: pd.DataFrame, engine: str, symbol: str, opt_side: str) -> List[Trade]:
    buy_s, sell_s = signals(x, engine)
    trades: List[Trade] = []
    pos = 0
    entry = sl = tp1 = tp2 = tp3 = np.nan
    entry_time = None
    hit1 = hit2 = False
    last_exit_i = -10_000
    trades_day = 0
    last_day = None

    for i in range(1, len(x)):
        ts = x.index[i]
        d0 = ts.date()
        if d0 != last_day:
            trades_day = 0
            last_day = d0
        row = x.iloc[i]
        side_ok = (not USE_SYNC) or (opt_side == "CE" and bool(row["undBull"])) or (opt_side == "PE" and bool(row["undBear"]))
        filters_ok = bool(row["filtersOk"])
        cool_ok = (i - last_exit_i) >= COOLDOWN
        day_ok = MAX_DAY == 0 or trades_day < MAX_DAY

        if pos == 0:
            if buy_s.iloc[i] and filters_ok and side_ok and cool_ok and day_ok:
                pos = 1
                entry = float(row["Close"])
                sl = entry - SL_PTS
                tp1, tp2, tp3 = entry + TP1, entry + TP2, entry + TP3
                entry_time = ts
                hit1 = hit2 = False
                trades_day += 1
            continue

        # manage
        hi, lo, cl = float(row["High"]), float(row["Low"]), float(row["Close"])
        reason = None
        exit_px = cl
        if sell_s.iloc[i]:
            reason, exit_px = "Engine SELL", cl
        if lo <= sl:
            reason, exit_px = "SL", sl
        if (not hit1) and hi >= tp1:
            hit1 = True
        if hit1 and (not hit2) and hi >= tp2:
            hit2 = True
        if hi >= tp3:
            reason, exit_px = "TP3", tp3
            hit3 = True
        else:
            hit3 = False

        if reason:
            # if SL and TP same bar, assume adverse first (conservative)
            if lo <= sl and hi >= tp1 and reason != "SL":
                # already set
                pass
            pnl = exit_px - entry
            trades.append(Trade(engine, symbol, opt_side, entry_time, ts, entry, exit_px, pnl, reason, hit1, hit2, reason == "TP3"))
            pos = 0
            last_exit_i = i
    return trades


ENGINES = [
    "E1 Swing Structure",
    "E2 Opening Range Breakout",
    "E3 VWAP Reclaim",
    "E4 Prev Day High/Low Break",
    "E5 Pullback Continuation",
    "E6 EMA Stack Momentum",
    "E7 ATR Expansion Impulse",
    "E8 RSI Regime",
    "E9 MACD Histogram",
    "E10 Supertrend",
    "E11 Engulf + Volume",
    "E12 Rejection Wick Sweep",
    "E13 Inside Bar Breakout",
    "E14 Round Premium Levels",
    "E15 Option CPR / Pivot",
    "E16 Donchian Channel Break",
    "E21 Bollinger Squeeze Break",
]


def summarize(trades: List[Trade]) -> dict:
    n = len(trades)
    if n == 0:
        return dict(trades=0, profit_trades=0, loss_trades=0, sl_hits=0, tp1=0, tp2=0, tp3=0,
                    engine_sell=0, net=0.0, win_rate=0.0, avg=0.0, profit_factor=0.0,
                    days_tp1_ok=0)
    pnl = np.array([t.pnl for t in trades])
    reasons = [t.reason for t in trades]
    profit_trades = int((pnl > 0).sum())
    loss_trades = int((pnl <= 0).sum())
    sl_hits = sum(1 for r in reasons if r == "SL")
    eng = sum(1 for r in reasons if r == "Engine SELL")
    tp3 = sum(1 for r in reasons if r == "TP3")
    tp1 = sum(1 for t in trades if t.hit_tp1)
    tp2 = sum(1 for t in trades if t.hit_tp2)
    wins = pnl[pnl > 0].sum()
    losses = -pnl[pnl <= 0].sum()
    pf = (wins / losses) if losses > 0 else float("inf") if wins > 0 else 0.0
    # days with at least one TP1 hit
    by_day = {}
    for t in trades:
        d = t.entry_time.date()
        by_day.setdefault(d, False)
        if t.hit_tp1:
            by_day[d] = True
    return dict(
        trades=n,
        profit_trades=profit_trades,
        loss_trades=loss_trades,
        sl_hits=sl_hits,
        tp1=tp1,
        tp2=tp2,
        tp3=tp3,
        engine_sell=eng,
        net=float(pnl.sum()),
        win_rate=100.0 * profit_trades / n,
        avg=float(pnl.mean()),
        profit_factor=float(pf) if pf != float("inf") else 999.0,
        days_tp1_ok=sum(1 for v in by_day.values() if v),
        trading_days=len(by_day),
    )


def main():
    all_trades: List[Trade] = []
    per_engine_rows = []
    per_symbol_engine = []

    print("Downloading index data…")
    raw = {}
    for name, tkr in SYMBOLS.items():
        raw[name] = download_5m(tkr)
        print(f"  {name}: {len(raw[name])} bars  {raw[name].index.min()} → {raw[name].index.max()}")

    for name, und in raw.items():
        for opt_side in ("CE", "PE"):
            print(f"Preparing {name} {opt_side}…")
            prem = build_synthetic_option(und, opt_side)
            x = prepare(prem, und)
            for eng in ENGINES:
                tr = run_engine(x, eng, name, opt_side)
                all_trades.extend(tr)
                s = summarize(tr)
                s.update(engine=eng, symbol=name, side=opt_side)
                per_symbol_engine.append(s)

    # aggregate by engine across all symbols/sides
    for eng in ENGINES:
        subset = [t for t in all_trades if t.engine == eng]
        s = summarize(subset)
        s["engine"] = eng
        per_engine_rows.append(s)

    eng_df = pd.DataFrame(per_engine_rows).sort_values("net", ascending=False)
    detail_df = pd.DataFrame(per_symbol_engine)
    trades_df = pd.DataFrame([t.__dict__ for t in all_trades])

    eng_df.to_csv("backtest_by_engine.csv", index=False)
    detail_df.to_csv("backtest_by_symbol_engine.csv", index=False)
    trades_df.to_csv("backtest_trades.csv", index=False)

    # overall
    overall = summarize(all_trades)
    profitable_engines = int((eng_df["net"] > 0).sum())
    losing_engines = int((eng_df["net"] <= 0).sum())
    # engines where SL hits > profit trades
    eng_df["sl_rate"] = np.where(eng_df["trades"] > 0, 100 * eng_df["sl_hits"] / eng_df["trades"], 0)

    # Write report
    lines = []
    lines.append("# Options Engines Lab — Backtest Report")
    lines.append("")
    lines.append("## Methodology (read this)")
    lines.append("")
    lines.append("- **Period:** ~60 trading days of **5-minute** bars (Yahoo Finance), IST session 09:15–15:29.")
    lines.append("- **Underlyings:** Nifty (`^NSEI`), BankNifty (`^NSEBANK`), Sensex (`^BSESN`).")
    lines.append("- **Option series:** Yahoo does **not** provide NSE CE/PE OHLC. Premiums are **synthetic ATM proxies** (≈0.5 delta track + mild theta) so TP1=10 / SL=12 are tested in *premium points*, not index points.")
    lines.append("- **Rules mirrored from** `Options_Engines_Lab.pine`: one engine at a time, TP1=10, TP2=20, TP3=35, SL=12, cooldown=5, max 6 entries/day, session + late-block + ADX chop filters, CE/PE sync via underlying EMA(9/21).")
    lines.append("- **Same-bar SL vs TP:** if both could hit, **SL is prioritized** (conservative).")
    lines.append("- This is a **relative ranking** of engines under one consistent model — not a guarantee of live NSE option PnL (IV crush, spreads, slippage not modeled).")
    lines.append("")
    lines.append("## Headline numbers")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|------:|")
    lines.append(f"| Signal engines tested | {len(ENGINES)} |")
    lines.append(f"| Engines with **net profit** | **{profitable_engines}** |")
    lines.append(f"| Engines with **net loss** | **{losing_engines}** |")
    lines.append(f"| Total trades (all engines × symbols × CE/PE) | {overall['trades']} |")
    lines.append(f"| Profitable trades (PnL > 0) | {overall['profit_trades']} ({100*overall['profit_trades']/max(overall['trades'],1):.1f}%) |")
    lines.append(f"| Losing trades | {overall['loss_trades']} |")
    lines.append(f"| **Stop-loss hits** | **{overall['sl_hits']}** ({100*overall['sl_hits']/max(overall['trades'],1):.1f}% of trades) |")
    lines.append(f"| Exits by engine SELL | {overall['engine_sell']} |")
    lines.append(f"| Trades that tagged TP1 (+10) | {overall['tp1']} |")
    lines.append(f"| Trades that tagged TP2 (+20) | {overall['tp2']} |")
    lines.append(f"| Full exits at TP3 (+35) | {overall['tp3']} |")
    lines.append(f"| Combined net premium pts (sum of all engines)* | {overall['net']:.1f} |")
    lines.append("")
    lines.append("\\*Combined net is **not** a realistic portfolio PnL (engines are alternatives, not run together). Use per-engine net below.")
    lines.append("")
    lines.append("## Per-engine leaderboard (all symbols + CE/PE combined)")
    lines.append("")
    lines.append("| Rank | Engine | Trades | Profit trades | Loss trades | SL hits | SL% | TP1 | TP2 | TP3 | Win% | Net pts | Avg pts |")
    lines.append("|-----:|--------|-------:|--------------:|------------:|--------:|----:|----:|----:|----:|-----:|--------:|--------:|")
    for i, r in enumerate(eng_df.itertuples(), 1):
        slpct = 100 * r.sl_hits / r.trades if r.trades else 0
        lines.append(
            f"| {i} | {r.engine} | {r.trades} | {r.profit_trades} | {r.loss_trades} | {r.sl_hits} | {slpct:.0f}% | {r.tp1} | {r.tp2} | {r.tp3} | {r.win_rate:.0f}% | {r.net:.1f} | {r.avg:.2f} |"
        )
    lines.append("")
    lines.append("## Profit vs Stop-Loss by engine")
    lines.append("")
    lines.append("| Engine | Result | Net pts | SL hits | Profit trades |")
    lines.append("|--------|--------|--------:|--------:|--------------:|")
    for r in eng_df.itertuples():
        res = "✅ PROFIT" if r.net > 0 else "❌ LOSS"
        lines.append(f"| {r.engine} | {res} | {r.net:.1f} | {r.sl_hits} | {r.profit_trades} |")
    lines.append("")

    # Best / worst
    best = eng_df.iloc[0]
    worst = eng_df.iloc[-1]
    most_sl = eng_df.sort_values("sl_hits", ascending=False).iloc[0]
    best_tp1 = eng_df.sort_values("tp1", ascending=False).iloc[0]
    lines.append("## Takeaways")
    lines.append("")
    lines.append(f"- **Best net engine:** {best.engine} — net **{best.net:.1f}** pts, SL hits {best.sl_hits}/{best.trades}, TP1 tags {best.tp1}.")
    lines.append(f"- **Worst net engine:** {worst.engine} — net **{worst.net:.1f}** pts, SL hits {worst.sl_hits}/{worst.trades}.")
    lines.append(f"- **Most stop-outs:** {most_sl.engine} — **{most_sl.sl_hits}** SL hits.")
    lines.append(f"- **Most TP1 (+10) tags:** {best_tp1.engine} — **{best_tp1.tp1}** times.")
    lines.append(f"- Engines in profit: **{profitable_engines}/{len(ENGINES)}**. Engines in loss: **{losing_engines}/{len(ENGINES)}**.")
    lines.append("")
    lines.append("## Breakdown by underlying (net pts of each engine)")
    lines.append("")
    pivot = detail_df.pivot_table(index="engine", columns="symbol", values="net", aggfunc="sum")
    # also CE/PE
    lines.append(pivot.round(1).to_markdown())
    lines.append("")
    lines.append("## CE vs PE (net pts summed across underlyings)")
    lines.append("")
    ce_pe = detail_df.groupby(["engine", "side"])["net"].sum().unstack("side")
    lines.append(ce_pe.round(1).to_markdown())
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- `backtest_by_engine.csv` — engine aggregates")
    lines.append("- `backtest_by_symbol_engine.csv` — per symbol/side")
    lines.append("- `backtest_trades.csv` — every trade")
    lines.append("- `backtest_options_engines_lab.py` — reproducible script")
    lines.append("")

    report = "\n".join(lines)
    open("BACKTEST_OPTIONS_ENGINES_LAB.md", "w").write(report)
    print("\n" + report)
    print("\nWrote BACKTEST_OPTIONS_ENGINES_LAB.md and CSVs.")


if __name__ == "__main__":
    main()
