"""Module housing all the enemy dragon classes."""
from dataclasses import dataclass

from dragonsweepyr.utils import res_to_frame


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


# Spells
class SpellMakeOrb(BoardTile):

    """Spell to make orb."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.SpellMakeOrb
        self.stripFrame = 10


class SpellRevealSlimes(BoardTile):

    """Spell to reveal slimes."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.SpellRevealSlimes
        self.stripFrame = 19


class SpellRevealRats(BoardTile):

    """Spell to reveal rats."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.SpellRevealRats
        self.stripFrame = 29


class SpellDisarm(BoardTile):

    """Spell to disarm."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.SpellDisarm
        self.stripFrame = 35


# Items
class Orb(BoardTile):

    """Orb item."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Orb
        self.stripFrame = 23


class Medikit(BoardTile):

    """Medikit item."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Medikit
        self.stripFrame = 22


class Crown(BoardTile):

    """Crown item."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Crown
        self.stripFrame = 142


class Treasure(BoardTile):

    """Treasure item."""

    def __init__(self, xp: int = 1) -> None:
        super().__init__()
        self.id = TileID.Treasure
        self.xp = xp
        if xp == 1:
            self.stripFrame = 30
        elif xp == 3:
            self.stripFrame = 31
        else:  # xp == 5
            self.stripFrame = 24


class Chest(BoardTile):

    """Chest item."""

    def __init__(self, contains: BoardTile | None = None) -> None:
        super().__init__()
        self.id = TileID.Chest
        self.stripFrame = res_to_frame(70, 360)
        self.contains = contains or Treasure(5)


# Monsters
class Dragon(BoardTile):

    """Dragon monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Dragon
        self.stripFrame = res_to_frame(200, 311)
        self.deadStripFrame = res_to_frame(230, 310)
        self.isMonster = True
        self.monsterLevel = 13
        self.xp = 13


class Fidel(BoardTile):

    """Fidel monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Fidel
        self.stripFrame = res_to_frame(0, 408)
        self.isMonster = True
        self.monsterLevel = 0
        self.xp = 0


class DragonEgg(BoardTile):

    """Dragon egg monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.DragonEgg
        self.stripFrame = res_to_frame(0, 250)
        self.deadStripFrame = self.stripFrame + 1
        self.isMonster = True
        self.monsterLevel = 0
        self.xp = 3


class RatKing(BoardTile):

    """Rat King monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.RatKing
        self.stripFrame = res_to_frame(70, 265)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Rat(BoardTile):

    """Rat monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Rat
        self.stripFrame = res_to_frame(90, 265)
        self.isMonster = True
        self.monsterLevel = 1
        self.xp = 1


class Bat(BoardTile):

    """Bat monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Bat
        self.stripFrame = res_to_frame(134, 231)
        self.isMonster = True
        self.monsterLevel = 2
        self.xp = 2


class Skeleton(BoardTile):

    """Skeleton monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Skeleton
        self.stripFrame = res_to_frame(70, 134)
        self.isMonster = True
        self.monsterLevel = 3
        self.xp = 3


class Guard(BoardTile):

    """Guard monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Guard
        self.stripFrame = res_to_frame(200, 200)
        self.isMonster = True
        self.monsterLevel = 7
        self.xp = 7


class Snake(BoardTile):

    """Snake monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Snake
        self.stripFrame = res_to_frame(250, 250)
        self.isMonster = True
        self.monsterLevel = 7
        self.xp = 7


class MineKing(BoardTile):

    """Mine King monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.MineKing
        self.stripFrame = res_to_frame(250, 135)
        self.isMonster = True
        self.monsterLevel = 10
        self.xp = 10


class Gazer(BoardTile):

    """Gazer monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Gazer
        self.stripFrame = res_to_frame(135, 180)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Slime(BoardTile):

    """Slime monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Slime
        self.stripFrame = res_to_frame(86, 473)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Wizard(BoardTile):

    """Wizard monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Wizard
        self.stripFrame = res_to_frame(72, 76)
        self.isMonster = True
        self.monsterLevel = 1
        self.xp = 1


class BigSlime(BoardTile):

    """Big Slime monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.BigSlime
        self.stripFrame = res_to_frame(120, 455)
        self.isMonster = True
        self.monsterLevel = 8
        self.xp = 8


class Minotaur(BoardTile):

    """Minotaur monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Minotaur
        self.stripFrame = res_to_frame(200, 326)
        self.isMonster = True
        self.monsterLevel = 6
        self.xp = 6


class Gargoyle(BoardTile):

    """Gargoyle monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Gargoyle
        self.stripFrame = res_to_frame(26, 210)
        self.isMonster = True
        self.monsterLevel = 4
        self.xp = 4


class Giant(BoardTile):

    """Giant monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Giant
        self.stripFrame = res_to_frame(0, 450)
        self.isMonster = True
        self.monsterLevel = 9
        self.xp = 9


class Gnome(BoardTile):

    """Gnome monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Gnome
        self.stripFrame = res_to_frame(40, 408)
        self.isMonster = True
        self.monsterLevel = 0
        self.xp = 9


class Mimic(BoardTile):

    """Mimic monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Mimic
        self.stripFrame = res_to_frame(70, 360)
        self.isMonster = True
        self.monsterLevel = 11
        self.xp = 11
        self.mimicMimicking = True


class Mine(BoardTile):

    """Mine monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Mine
        self.stripFrame = res_to_frame(150, 455)
        self.deadStripFrame = res_to_frame(170, 455)
        self.isMonster = True
        self.monsterLevel = 100
        self.xp = 3


class Death(BoardTile):

    """Death monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Death
        self.stripFrame = res_to_frame(130, 340)
        self.isMonster = True
        self.monsterLevel = 9
        self.xp = 9


class DarkKnight(BoardTile):

    """Dark Knight monster."""

    def __init__(self, level: int = 5) -> None:
        super().__init__()
        self.id = TileID.DarkKnight
        self.isMonster = True
        self.monsterLevel = level
        self.xp = level
        if level == 5:
            self.stripFrame = res_to_frame(200, 168)
        else:  # level == 7
            self.stripFrame = res_to_frame(200, 100)


class Eye(BoardTile):

    """Eye monster."""

    def __init__(self) -> None:
        super().__init__()
        self.id = TileID.Eye
        self.stripFrame = res_to_frame(135, 167)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5
