"""BoardTile child classes for spells"""
from dragonsweepyr.monsters.tiles import BoardTile, TileID


class SpellDisarm(BoardTile):

    """Spell to disarm."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.SpellDisarm
        self.strip_frame = 35


class SpellMakeOrb(BoardTile):

    """Spell to make orb."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.SpellMakeOrb
        self.strip_frame = 10


class SpellRevealRats(BoardTile):

    """Spell to reveal rats."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.SpellRevealRats
        self.strip_frame = 29


class SpellRevealSlimes(BoardTile):

    """Spell to reveal slimes."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.SpellRevealSlimes
        self.strip_frame = 19
