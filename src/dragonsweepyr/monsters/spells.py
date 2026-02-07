"""
Factory functions for creating spell entities.

All spell entities are now created through the data-driven entity system.
See entity_definitions.py for entity configuration.
"""

from dragonsweepyr.monsters.entity_definitions import entity_factory
from dragonsweepyr.monsters.tiles import TileID


def SpellDisarm():
    """Create a SpellDisarm spell."""
    return entity_factory.create(TileID.SpellDisarm)


def SpellMakeOrb():
    """Create a SpellMakeOrb spell."""
    return entity_factory.create(TileID.SpellMakeOrb)


def SpellRevealRats():
    """Create a SpellRevealRats spell."""
    return entity_factory.create(TileID.SpellRevealRats)


def SpellRevealSlimes():
    """Create a SpellRevealSlimes spell."""
    return entity_factory.create(TileID.SpellRevealSlimes)
