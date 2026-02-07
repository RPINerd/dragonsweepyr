"""
Factory functions for creating item entities.

All item entities are now created through the data-driven entity system.
See entity_definitions.py for entity configuration.
"""

from dragonsweepyr.monsters.entity_definitions import entity_factory
from dragonsweepyr.monsters.tiles import TileID


def Chest(contains=None):
    """Create a Chest item."""
    tile = entity_factory.create(TileID.Chest)
    tile.contains = contains or Treasure(5)
    return tile


def Crown():
    """Create a Crown item."""
    return entity_factory.create(TileID.Crown)


def Medikit():
    """Create a Medikit item."""
    return entity_factory.create(TileID.Medikit)


def Orb():
    """Create an Orb item."""
    return entity_factory.create(TileID.Orb)


def Treasure(xp: int = 1):
    """Create a Treasure item."""
    tile = entity_factory.create(TileID.Treasure)
    tile.xp = xp
    # Adjust sprite based on xp value
    if xp == 1:
        tile.strip_frame = 30
    elif xp == 3:
        tile.strip_frame = 31
    else:  # xp == 5
        tile.strip_frame = 24
    return tile
