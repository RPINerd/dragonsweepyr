"""Utility functions for small operations throuout the code"""

from math import pi, sqrt


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """distance"""
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def dist_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """distSquared"""
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


def is_level_halfheart(level: int) -> bool:
    """isLevelHalfHeart"""
    return level % 2 == 0


def lerp(a: float, b: float, alpha: float) -> float:
    """lerp"""
    return a + alpha * (b - a)


def rad_to_deg(r: float) -> float:
    """r2d"""
    return 180 * r / pi


def res_to_frame(x: int, y: int) -> int:
    """stripXYToFrame"""
    return (x // 16) + (y // 16) * 16


def res_to_frame24(x: int, y: int) -> int:
    """stripXYToFrame24"""
    return (x // 24) + (y // 24) * 10


def xp_to_next_level(level: int) -> int:
    """
    Return the number of XP required to reach the next level

    Level: 1   2  3  4  5   6   7   8   9  10  11  12  13  14  15
    HP:    5      6     7       8       9      10      11      12
    """
    xp_lookup = [0, 4, 5, 7, 9, 9, 10, 12, 12, 12, 15, 18, 21, 21, 25]
    player_stat = min(level, len(xp_lookup) - 1)
    return xp_lookup[player_stat]
