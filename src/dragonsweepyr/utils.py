"""Utility functions for small operations throuout the code"""

from math import pi, sqrt

from dragonsweepyr.config import config


def clamp(v: float) -> float:
    """clamp01"""
    return max(0, min(1, v))


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """distance"""
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def dist_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """distSquared"""
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


def is_center(tx: int, ty: int) -> bool:
    """
    Validates if the given tile coordinates are in the center region of the grid.

    JavaScript Source: isCenter(tx, ty)

    Args:
        tx: Tile x-coordinate
        ty: Tile y-coordinate
    Returns:
        True if the tile is in the center region, False otherwise.
    """
    center_x = config.grid_columns // 2
    center_y = config.grid_rows // 2
    return (center_x == tx and ty == center_y)


def is_close_to_edge(tx: int, ty: int) -> bool:
    """
    Validates if the given tile coordinates are close to the edge of the grid.

    JavaScript Source: isCloseToEdge(tx, ty)

    Args:
        tx: Tile x-coordinate
        ty: Tile y-coordinate
    Returns:
        True if the tile is close to the edge, False otherwise.
    """
    return tx <= 1 or ty <= 1 or tx >= config.grid_columns - 2 or ty >= config.grid_rows - 2


def is_corner(tx: int, ty: int) -> bool:
    """
    Validates if the given tile coordinates are a corner of the grid.

    JavaScript Source: isCorner(tx, ty)

    Args:
        tx: Tile x-coordinate
        ty: Tile y-coordinate
    Returns:
        True if the tile is a corner, False otherwise.
    """
    top_left = (tx == 0 and ty == 0)
    top_right = (tx == config.grid_columns - 1 and ty == 0)
    bottom_left = (tx == 0 and ty == config.grid_rows - 1)
    bottom_right = (tx == config.grid_columns - 1 and ty == config.grid_rows - 1)
    return any([top_left, top_right, bottom_left, bottom_right])


def is_edge(tx: int, ty: int) -> bool:
    """
    Validates if the given tile coordinates are on the edge of the grid.

    JavaScript Source: isEdge(tx, ty)

    Args:
        tx: Tile x-coordinate
        ty: Tile y-coordinate

    Returns:
        True if the tile is on the edge, False otherwise.
    """
    return tx == 0 or ty == 0 or tx == config.grid_columns - 1 or ty == config.grid_rows - 1


def is_level_halfheart(level: int) -> bool:
    """isLevelHalfHeart"""
    return level % 2 == 0


def lerp(a: float, b: float, alpha: float) -> float:
    """lerp"""
    return a + alpha * (b - a)


def rad_to_deg(r: float) -> float:
    """
    Convert radians to degrees

    JavaScript Source: r2d(r)

    Args:
        r: Angle in radians

    Returns:
        Angle in degrees
    """
    return 180 * r / pi


def res_to_frame(x: int, y: int) -> int:
    """stripXYToFrame"""
    return (x // 16) + (y // 16) * 16


def res_to_frame24(x: int, y: int) -> int:
    """stripXYToFrame24"""
    return (x // 24) + (y // 24) * 10
