"""Base class for tile entities and decorations"""
from dataclasses import dataclass

from dragonsweepyr.utils import distance


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


class BoardTile:

    """Represents a single tile on the game board."""

    def __init__(self) -> None:
        """"""
        self.tx = 0
        self.ty = 0
        self.fixed = False
        self.id = TileID.Empty
        self.strip = None
        self.stripFrame = 1  # Default to empty sprite
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

    def is_empty(self) -> bool:
        """Check if the tile is empty."""
        return self.id == TileID.Empty

    def is_near(self, other: "BoardTile", dist: int | float = 1) -> bool:
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
        return 0

    def on_reveal(self) -> None:
        """Called when the tile is revealed."""
        pass
