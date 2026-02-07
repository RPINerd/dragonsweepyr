"""
Factory functions for creating creature entities.

All creature entities are now created through the data-driven entity system.
See entity_definitions.py for entity configuration.
"""

from dragonsweepyr.monsters.entity_definitions import entity_factory
from dragonsweepyr.monsters.tiles import TileID


def Bat(monster_level: int = 2):
    """Create a Bat creature."""
    tile = entity_factory.create(TileID.Bat)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def BigSlime(monster_level: int = 8):
    """Create a BigSlime creature."""
    tile = entity_factory.create(TileID.BigSlime)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def DarkKnight(monster_level: int = 5):
    """Create a DarkKnight creature."""
    tile = entity_factory.create(TileID.DarkKnight)
    tile.monster_level = monster_level
    tile.xp = monster_level
    # Adjust sprite based on level
    if monster_level == 5:
        from dragonsweepyr.monsters.entity_definitions import _get_frame
        tile.strip_frame = _get_frame("dark_knight_level5")
    else:  # level 7
        from dragonsweepyr.monsters.entity_definitions import _get_frame
        tile.strip_frame = _get_frame("dark_knight_level7")
    return tile


def Death(monster_level: int = 9):
    """Create a Death creature."""
    tile = entity_factory.create(TileID.Death)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Dragon(monster_level: int = 13):
    """Create a Dragon creature."""
    tile = entity_factory.create(TileID.Dragon)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def DragonEgg(monster_level: int = 0):
    """Create a DragonEgg creature."""
    tile = entity_factory.create(TileID.DragonEgg)
    tile.monster_level = monster_level
    tile.xp = 3
    return tile


def Eye(monster_level: int = 5):
    """Create an Eye creature."""
    tile = entity_factory.create(TileID.Eye)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Fidel(monster_level: int = 0):
    """Create a Fidel creature."""
    tile = entity_factory.create(TileID.Fidel)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Gargoyle(monster_level: int = 4):
    """Create a Gargoyle creature."""
    tile = entity_factory.create(TileID.Gargoyle)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Gazer(monster_level: int = 5):
    """Create a Gazer creature."""
    tile = entity_factory.create(TileID.Gazer)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Giant(monster_level: int = 9):
    """Create a Giant creature."""
    tile = entity_factory.create(TileID.Giant)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Gnome(monster_level: int = 0):
    """Create a Gnome creature."""
    tile = entity_factory.create(TileID.Gnome)
    tile.monster_level = monster_level
    tile.xp = 9
    return tile


def Guard(monster_level: int = 7):
    """Create a Guard creature."""
    tile = entity_factory.create(TileID.Guard)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Mimic(monster_level: int = 11):
    """Create a Mimic creature."""
    tile = entity_factory.create(TileID.Mimic)
    tile.monster_level = monster_level
    tile.xp = monster_level
    tile.mimicMimicking = True
    return tile


def Mine(monster_level: int = 100):
    """Create a Mine creature."""
    tile = entity_factory.create(TileID.Mine)
    tile.monster_level = monster_level
    tile.xp = 3
    return tile


def MineKing(monster_level: int = 10):
    """Create a MineKing creature."""
    tile = entity_factory.create(TileID.MineKing)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Minotaur(monster_level: int = 6):
    """Create a Minotaur creature."""
    tile = entity_factory.create(TileID.Minotaur)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Rat(monster_level: int = 1):
    """Create a Rat creature."""
    tile = entity_factory.create(TileID.Rat)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def RatKing(monster_level: int = 5):
    """Create a RatKing creature."""
    tile = entity_factory.create(TileID.RatKing)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Skeleton(monster_level: int = 3):
    """Create a Skeleton creature."""
    tile = entity_factory.create(TileID.Skeleton)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Slime(monster_level: int = 5):
    """Create a Slime creature."""
    tile = entity_factory.create(TileID.Slime)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Snake(monster_level: int = 7):
    """Create a Snake creature."""
    tile = entity_factory.create(TileID.Snake)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile


def Wizard(monster_level: int = 1):
    """Create a Wizard creature."""
    tile = entity_factory.create(TileID.Wizard)
    tile.monster_level = monster_level
    tile.xp = monster_level
    return tile
