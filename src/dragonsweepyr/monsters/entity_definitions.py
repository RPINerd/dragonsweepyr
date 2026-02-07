"""Data-driven entity definitions and registry for sprite management."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from dragonsweepyr.monsters.tiles import TileID
from dragonsweepyr.utils import is_center, is_close_to_edge, is_corner, is_edge

if TYPE_CHECKING:
    from dragonsweepyr.monsters.tiles import BoardTile


@dataclass
class EntityDef:

    """Definition for a game entity sprite."""

    id: int
    name: str
    sprite_frame: int
    is_monster: bool = False
    monster_level: int = 0
    xp: int = 0
    dead_frame: int = 0
    satisfaction_func: Callable[[BoardTile], int] | None = None
    metadata: dict = field(default_factory=dict)


def _load_sprite_coords() -> dict:
    """Load sprite coordinates from JSON file."""
    coords_path = Path(__file__).parent / "sprite_coords.json"
    with Path(coords_path).open() as f:
        return json.load(f)


# Load sprite coordinates at module level
_SPRITE_COORDS = _load_sprite_coords()


def _get_frame(sprite_name: str) -> int:
    """Get sprite frame from sprite_coords.json."""
    if sprite_name in _SPRITE_COORDS:
        return _SPRITE_COORDS[sprite_name]["frame"]
    return 0


# Satisfaction functions for entities with special placement rules
def _dragon_satisfaction(tile: BoardTile) -> int:
    """Dragons should be in a central region of the board."""
    return 10000 if is_center(tile.tx, tile.ty) else 0


def _fidel_satisfaction(tile: BoardTile) -> int:
    """Fidel prefers corners."""
    return 9000 if is_corner(tile.tx, tile.ty) else 0


def _mine_king_satisfaction(tile: BoardTile) -> int:
    """The Mine King must be in a corner."""
    return 10000 if is_corner(tile.tx, tile.ty) else 0


def _wizard_satisfaction(tile: BoardTile) -> int:
    """Wizards should be along an edge but not in a corner."""
    return 10000 if is_edge(tile.tx, tile.ty) and not is_corner(tile.tx, tile.ty) else 0


def _orb_satisfaction(tile: BoardTile) -> int:
    """Orb cannot be placed near an edge."""
    return -10000 if is_close_to_edge(tile.tx, tile.ty) else 0


def _guard_satisfaction(tile: BoardTile) -> int:
    """Guards should be in respective quadrants based on their name."""
    match tile.name:
        case "guard1":
            return 2500 if tile.tx < 6 and tile.ty < 4 else 0
        case "guard2":
            return 2500 if tile.tx > 6 and tile.ty < 4 else 0
        case "guard3":
            return 2500 if tile.tx > 6 and tile.ty > 4 else 0
        case "guard4":
            return 2500 if tile.tx < 6 and tile.ty > 4 else 0
        case _:
            return 0


# Entity registry - all entities defined as data
ENTITY_REGISTRY: dict[int, EntityDef] = {
    # Creatures/Monsters
    TileID.Bat: EntityDef(
        id=TileID.Bat,
        name="Bat",
        sprite_frame=_get_frame("bat"),
        is_monster=True,
        monster_level=2,
        xp=2,
    ),
    TileID.BigSlime: EntityDef(
        id=TileID.BigSlime,
        name="BigSlime",
        sprite_frame=_get_frame("big_slime"),
        is_monster=True,
        monster_level=8,
        xp=8,
    ),
    TileID.DarkKnight: EntityDef(
        id=TileID.DarkKnight,
        name="DarkKnight",
        sprite_frame=_get_frame("dark_knight_level5"),
        is_monster=True,
        monster_level=5,
        xp=5,
        metadata={"alt_frames": {"level5": _get_frame("dark_knight_level5"), "level7": _get_frame("dark_knight_level7")}},
    ),
    TileID.Death: EntityDef(
        id=TileID.Death,
        name="Death",
        sprite_frame=_get_frame("death"),
        is_monster=True,
        monster_level=9,
        xp=9,
    ),
    TileID.Dragon: EntityDef(
        id=TileID.Dragon,
        name="Dragon",
        sprite_frame=_get_frame("dragon"),
        is_monster=True,
        monster_level=13,
        xp=13,
        dead_frame=_get_frame("dragon_dead"),
        satisfaction_func=_dragon_satisfaction,
    ),
    TileID.DragonEgg: EntityDef(
        id=TileID.DragonEgg,
        name="DragonEgg",
        sprite_frame=_get_frame("dragon_egg"),
        is_monster=True,
        monster_level=0,
        xp=3,
        dead_frame=_get_frame("dragon_egg_dead"),
    ),
    TileID.Eye: EntityDef(
        id=TileID.Eye,
        name="Eye",
        sprite_frame=_get_frame("eye"),
        is_monster=True,
        monster_level=5,
        xp=5,
    ),
    TileID.Fidel: EntityDef(
        id=TileID.Fidel,
        name="Fidel",
        sprite_frame=_get_frame("fidel"),
        is_monster=True,
        monster_level=0,
        xp=0,
        satisfaction_func=_fidel_satisfaction,
    ),
    TileID.Gargoyle: EntityDef(
        id=TileID.Gargoyle,
        name="Gargoyle",
        sprite_frame=_get_frame("gargoyle"),
        is_monster=True,
        monster_level=4,
        xp=4,
    ),
    TileID.Gazer: EntityDef(
        id=TileID.Gazer,
        name="Gazer",
        sprite_frame=_get_frame("gazer"),
        is_monster=True,
        monster_level=5,
        xp=5,
    ),
    TileID.Giant: EntityDef(
        id=TileID.Giant,
        name="Giant",
        sprite_frame=_get_frame("giant"),
        is_monster=True,
        monster_level=9,
        xp=9,
    ),
    TileID.Gnome: EntityDef(
        id=TileID.Gnome,
        name="Gnome",
        sprite_frame=_get_frame("gnome"),
        is_monster=True,
        monster_level=0,
        xp=9,
    ),
    TileID.Guard: EntityDef(
        id=TileID.Guard,
        name="Guard",
        sprite_frame=_get_frame("guard"),
        is_monster=True,
        monster_level=7,
        xp=7,
        satisfaction_func=_guard_satisfaction,
        metadata={"alt_frames": {
            "guard1": _get_frame("guard1"),
            "guard2": _get_frame("guard2"),
            "guard3": _get_frame("guard3"),
            "guard4": _get_frame("guard4"),
        }},
    ),
    TileID.Mimic: EntityDef(
        id=TileID.Mimic,
        name="Mimic",
        sprite_frame=_get_frame("mimic"),
        is_monster=True,
        monster_level=11,
        xp=11,
        metadata={"alt_frames": {"alternate": _get_frame("mimic_alternate")}},
    ),
    TileID.Mine: EntityDef(
        id=TileID.Mine,
        name="Mine",
        sprite_frame=_get_frame("mine"),
        is_monster=True,
        monster_level=100,
        xp=3,
        dead_frame=_get_frame("mine_dead"),
    ),
    TileID.MineKing: EntityDef(
        id=TileID.MineKing,
        name="MineKing",
        sprite_frame=_get_frame("mine_king"),
        is_monster=True,
        monster_level=10,
        xp=10,
        satisfaction_func=_mine_king_satisfaction,
    ),
    TileID.Minotaur: EntityDef(
        id=TileID.Minotaur,
        name="Minotaur",
        sprite_frame=_get_frame("minotaur"),
        is_monster=True,
        monster_level=6,
        xp=6,
    ),
    TileID.Rat: EntityDef(
        id=TileID.Rat,
        name="Rat",
        sprite_frame=_get_frame("rat"),
        is_monster=True,
        monster_level=1,
        xp=1,
    ),
    TileID.RatKing: EntityDef(
        id=TileID.RatKing,
        name="RatKing",
        sprite_frame=_get_frame("rat_king"),
        is_monster=True,
        monster_level=5,
        xp=5,
    ),
    TileID.Skeleton: EntityDef(
        id=TileID.Skeleton,
        name="Skeleton",
        sprite_frame=_get_frame("skeleton"),
        is_monster=True,
        monster_level=3,
        xp=3,
    ),
    TileID.Slime: EntityDef(
        id=TileID.Slime,
        name="Slime",
        sprite_frame=_get_frame("slime"),
        is_monster=True,
        monster_level=5,
        xp=5,
    ),
    TileID.Snake: EntityDef(
        id=TileID.Snake,
        name="Snake",
        sprite_frame=_get_frame("snake"),
        is_monster=True,
        monster_level=7,
        xp=7,
    ),
    TileID.Wizard: EntityDef(
        id=TileID.Wizard,
        name="Wizard",
        sprite_frame=_get_frame("wizard"),
        is_monster=True,
        monster_level=1,
        xp=1,
        satisfaction_func=_wizard_satisfaction,
    ),
    # Items
    TileID.Chest: EntityDef(
        id=TileID.Chest,
        name="Chest",
        sprite_frame=_get_frame("chest"),
        is_monster=False,
    ),
    TileID.Crown: EntityDef(
        id=TileID.Crown,
        name="Crown",
        sprite_frame=142,
        is_monster=False,
    ),
    TileID.Medikit: EntityDef(
        id=TileID.Medikit,
        name="Medikit",
        sprite_frame=22,
        is_monster=False,
    ),
    TileID.Orb: EntityDef(
        id=TileID.Orb,
        name="Orb",
        sprite_frame=23,
        is_monster=False,
        satisfaction_func=_orb_satisfaction,
    ),
    TileID.Treasure: EntityDef(
        id=TileID.Treasure,
        name="Treasure",
        sprite_frame=24,
        is_monster=False,
        metadata={"alt_frames": {"xp1": 30, "xp3": 31, "xp5": 24}},
    ),
    # Obstacles/Structures
    TileID.Wall: EntityDef(
        id=TileID.Wall,
        name="Wall",
        sprite_frame=11,
        is_monster=False,
    ),
    TileID.Decoration: EntityDef(
        id=TileID.Decoration,
        name="Decoration",
        sprite_frame=0,
        is_monster=False,
    ),
    # Spells
    TileID.SpellDisarm: EntityDef(
        id=TileID.SpellDisarm,
        name="SpellDisarm",
        sprite_frame=35,
        is_monster=False,
    ),
    TileID.SpellMakeOrb: EntityDef(
        id=TileID.SpellMakeOrb,
        name="SpellMakeOrb",
        sprite_frame=10,
        is_monster=False,
    ),
    TileID.SpellRevealRats: EntityDef(
        id=TileID.SpellRevealRats,
        name="SpellRevealRats",
        sprite_frame=29,
        is_monster=False,
    ),
    TileID.SpellRevealSlimes: EntityDef(
        id=TileID.SpellRevealSlimes,
        name="SpellRevealSlimes",
        sprite_frame=19,
        is_monster=False,
    ),
}


class EntityFactory:

    """Factory for creating board tiles from entity definitions."""

    def __init__(self):
        """Initialize the factory."""
        self.registry = ENTITY_REGISTRY

    def get_definition(self, tile_id: int) -> EntityDef | None:
        """Get entity definition by ID."""
        return self.registry.get(tile_id)

    def create(self, tile_id: int, **kwargs) -> BoardTile:
        """
        Create a board tile from an entity definition.

        Args:
            tile_id: The TileID to create.
            **kwargs: Additional arguments to pass to the BoardTile constructor.

        Returns:
            A BoardTile instance initialized from the entity definition.

        Raises:
            ValueError: If tile_id is not in the registry.
        """
        from dragonsweepyr.monsters.tiles import BoardTile

        definition = self.get_definition(tile_id)
        if not definition:
            raise ValueError(f"Unknown entity ID: {tile_id}")

        tile = BoardTile()
        tile.load_from_def(definition)

        # Apply any additional kwargs
        for key, value in kwargs.items():
            if hasattr(tile, key):
                setattr(tile, key, value)

        return tile

    def create_by_name(self, name: str, **kwargs) -> BoardTile:
        """
        Create a board tile by entity name.

        Args:
            name: The entity name (e.g., "Bat", "Dragon").
            **kwargs: Additional arguments to pass to the BoardTile constructor.

        Returns:
            A BoardTile instance.

        Raises:
            ValueError: If name is not found in registry.
        """
        for definition in self.registry.values():
            if definition.name == name:
                return self.create(definition.id, **kwargs)
        raise ValueError(f"Unknown entity name: {name}")


# Global factory instance
entity_factory = EntityFactory()
