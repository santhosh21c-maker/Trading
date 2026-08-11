#!/usr/bin/env python3
"""Sanity-check Decider/Target ladder math documented in README."""

from __future__ import annotations


def ladder(h: float, l: float, c: float, base_frac: float = 0.382, decider_frac: float = 0.06) -> dict[str, float]:
    centre = (h + l + c) / 3.0
    base = (h - l) * base_frac
    ratios = (1.0, 1.54, 1.83, 2.08)

    levels: dict[str, float] = {
        "C": centre,
        "B": base,
        "decider_high": centre + decider_frac * base,
        "decider_low": centre - decider_frac * base,
    }
    for idx, ratio in enumerate(ratios, start=1):
        levels[f"up_target_{idx}"] = centre + ratio * base
        levels[f"down_target_{idx}"] = centre - ratio * base
    return levels


def main() -> None:
    # Representative Nifty option premium window (illustrative values).
    h, l, c = 142.5, 118.0, 130.25
    levels = ladder(h, l, c)

    decider_gap = levels["decider_high"] - levels["decider_low"]
    expected_gap = 0.12 * levels["B"]
    assert abs(decider_gap - expected_gap) < 1e-9, f"Decider gap {decider_gap} != 0.12*B {expected_gap}"

    assert abs(levels["up_target_1"] - levels["C"] - levels["B"]) < 1e-9
    assert abs(levels["C"] - levels["down_target_1"] - levels["B"]) < 1e-9

    # Target 2 distance ratio from centre should match documented 1.54.
    ratio_t2 = (levels["up_target_2"] - levels["C"]) / levels["B"]
    assert abs(ratio_t2 - 1.54) < 1e-9

    print("Ladder math OK for sample window:")
    print(f"  C={levels['C']:.4f}  B={levels['B']:.4f}")
    print(f"  Decider gap = {decider_gap:.4f} (0.12*B)")
    print(f"  Up Target 1 = {levels['up_target_1']:.4f}")
    print(f"  Up Target 2 = {levels['up_target_2']:.4f} (ratio {ratio_t2:.2f})")


if __name__ == "__main__":
    main()
