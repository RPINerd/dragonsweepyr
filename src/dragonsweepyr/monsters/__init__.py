"""
Monster/entity system with data-driven sprite management.

This module provides factory functions and utilities for creating game entities
(creatures, items, obstacles, spells) with automatic sprite data loading.

The entity_factory can be used to create sprites by ID or name:
    from dragonsweepyr.monsters import entity_factory
    bat = entity_factory.create(TileID.Bat)
    dragon = entity_factory.create_by_name("Dragon")

All entity definitions are stored as data in entity_definitions.py,
making it easy to update sprites and properties across the entire system.
"""

from dragonsweepyr.monsters.entity_definitions import (
    ENTITY_REGISTRY,
    EntityDef,
    EntityFactory,
    entity_factory,
)
from dragonsweepyr.monsters.tiles import BoardTile, TileID

__all__ = [
    "ENTITY_REGISTRY",
    "BoardTile",
    "EntityDef",
    "EntityFactory",
    "TileID",
    "entity_factory",
]
