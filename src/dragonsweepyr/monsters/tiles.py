"""Base class for tile entities and decorations"""
from dataclasses import dataclass

from dragonsweepyr.utils import distance


@dataclass
class TileID:

    """Dataset of possible tile IDs."""

    NaN: str = "none"
    Empty: str = "empty"
    Orb: str = "orb"
    SpellMakeOrb: str = "spell_reveal"
    Mine: str = "mine"
    MineKing: str = "mine king"
    Dragon: str = "dragon"
    Wall: str = "wall"
    Mimic: str = "mimic"
    Medikit: str = "medikit"
    RatKing: str = "rat king"
    Rat: str = "rat"
    Slime: str = "slime"
    Gargoyle: str = "gargoyle"
    Minotaur: str = "minotaur"
    Chest: str = "chest"
    Skeleton: str = "skeleton"
    Treasure: str = "treasure"
    Snake: str = "snake"
    Giant: str = "giant"
    Decoration: str = "decoration"
    Wizard: str = "wizard"
    Gazer: str = "gazer"
    SpellDisarm: str = "spell_disarm"
    BigSlime: str = "big slime"
    SpellRevealRats: str = "spell_reveal_rats"
    SpellRevealSlimes: str = "spell_reveal_slimes"
    Gnome: str = "gnome"
    Bat: str = "bat"
    Guard: str = "guardian"
    Crown: str = "crown"
    Fidel: str = "fidel"
    DragonEgg: str = "dragon_egg"
    Death: str = "death"
    DarkKnight: str = "dark knight"
    Eye: str = "eye"


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
        self.monsterLevel = 0
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

    def is_near(self, other: "BoardTile", dist: int = 1) -> bool:
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

    def on_reveal(self) -> None:
        """Called when the tile is revealed."""
        pass


class Decoration(BoardTile):

    """Decoration tile."""

    def __init__(self, strip=None, frame: int = 0) -> None:
        super().__init__()
        self.id = TileID.Decoration
        self.strip = strip
        self.stripFrame = frame


class Wall(BoardTile):

    """Wall tile."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Wall
        self.stripFrame = 11
