"""
Factory functions for creating obstacle/structure entities.

All obstacle entities are now created through the data-driven entity system.
See entity_definitions.py for entity configuration.
"""

from dragonsweepyr.monsters.entity_definitions import entity_factory
from dragonsweepyr.monsters.tiles import TileID


def Decoration(strip=None, frame: int = 0):
    """Create a Decoration tile."""
    tile = entity_factory.create(TileID.Decoration)
    tile.strip = strip
    tile.strip_frame = frame
    return tile


def Wall(contains=None):
    """Create a Wall tile."""
    tile = entity_factory.create(TileID.Wall)
    tile.contains = contains
    return tile
