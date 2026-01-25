"""BoardTile child classes for items"""

from dragonsweepyr.monsters.tiles import BoardTile, TileID
from dragonsweepyr.utils import res_to_frame


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
