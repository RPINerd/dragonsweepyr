"""Base class for tile entities and decorations"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from dragonsweepyr.resources import assets
from dragonsweepyr.utils import distance

if TYPE_CHECKING:
    from dragonsweepyr.monsters.entity_definitions import EntityDef
    from dragonsweepyr.resources import SpriteSheet


@dataclass
class TileID:

    """Dataset of possible tile IDs."""

    NaN: int = -1
    Empty: int = 0
    Orb: int = 1
    SpellMakeOrb: int = 2
    Mine: int = 3
    MineKing: int = 4
    Dragon: int = 5
    Wall: int = 6
    Mimic: int = 7
    Medikit: int = 8
    RatKing: int = 9
    Rat: int = 10
    Slime: int = 11
    Gargoyle: int = 12
    Minotaur: int = 13
    Chest: int = 14
    Skeleton: int = 15
    Treasure: int = 16
    Snake: int = 17
    Giant: int = 18
    Decoration: int = 19
    Wizard: int = 20
    Gazer: int = 21
    SpellDisarm: int = 22
    BigSlime: int = 23
    SpellRevealRats: int = 24
    SpellRevealSlimes: int = 25
    Gnome: int = 26
    Bat: int = 27
    Guard: int = 28
    Crown: int = 29
    Fidel: int = 30
    DragonEgg: int = 31
    Death: int = 32
    DarkKnight: int = 33
    Eye: int = 34


class BoardTile(pygame.sprite.Sprite):

    """Represents a single tile on the game board."""

    def __init__(self) -> None:
        """Initialize the board tile."""
        self.tx = 0
        self.ty = 0
        self.fixed = False
        self.id = TileID.Empty
        self.image: pygame.Surface = assets.blank_sprite
        self.rect: pygame.Rect = self.image.get_rect()
        self.strip: SpriteSheet | None = None
        self.strip_frame = 1  # Default to empty sprite
        self.deadStripFrame = 0
        self.revealed = False
        self.monster_level = 0
        self.xp = 0
        self.mimicMimicking = False  # TODO: necessary
        self.defeated = False
        self.mark = 0
        self.trapDisarmed = False
        self.contains = None
        self.wallHP = 0
        self.wallMaxHP = 0
        self.isMonster = False
        self.name = "none"
        self.minotaurChestLocation = [-1, -1]
        self._satisfaction_func = None

    def load_from_def(self, definition: EntityDef) -> None:
        """
        Initialize tile from entity definition.

        Args:
            definition: EntityDef containing sprite and entity data.
        """
        self.id = definition.id
        self.strip_frame = definition.sprite_frame
        self.isMonster = definition.is_monster
        self.monster_level = definition.monster_level
        self.xp = definition.xp
        self.deadStripFrame = definition.dead_frame
        self._satisfaction_func = definition.satisfaction_func
        self.name = definition.name.lower()

    def set_frame(self, frame: int) -> None:
        """Set the frame of the tile's sprite strip."""
        self.strip_frame = frame

    def is_empty(self) -> bool:
        """Check if the tile is empty."""
        return self.id == TileID.Empty

    def is_near(self, other: BoardTile, dist: int | float = 1) -> bool:
        """
        Check if this tile is near to another tile.

        Javascript Source: isCloseTo(a, actorId, dist)

        Args:
            other (BoardTile): The other tile to check against.
            dist (int): The maximum distance to consider as "near".

        Returns:
            bool: True if the tiles are near, False otherwise.
        """
        return distance(self.tx, self.ty, other.tx, other.ty) <= dist

    def satisfaction(self) -> int:
        """
        Calculate the satisfaction value of the tile.

        Returns:
            An integer representing the satisfaction value.
        """
        if self._satisfaction_func:
            return self._satisfaction_func(self)
        return 0

    def on_reveal(self) -> None:
        """Called when the tile is revealed."""
        pass
