"""BoardTile child classes for items"""

from dragonsweepyr.monsters.tiles import BoardTile, TileID
from dragonsweepyr.utils import is_close_to_edge, res_to_frame


class Chest(BoardTile):

    """Chest item."""

    def __init__(self, contains: BoardTile | None = None) -> None:
        """"""
        super().__init__()
        self.id = TileID.Chest
        self.strip_frame = res_to_frame(70, 360)
        self.contains = contains or Treasure(5)

    def satisfaction(self) -> int:
        """Chests have no locational satisfaction effect."""
        return super().satisfaction()


class Crown(BoardTile):

    """Crown item."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Crown
        self.strip_frame = 142

    def satisfaction(self) -> int:
        """Crowns have no locational satisfaction effect."""
        return super().satisfaction()


class Medikit(BoardTile):

    """Medikit item."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Medikit
        self.strip_frame = 22

    def satisfaction(self) -> int:
        """Medikits have no locational satisfaction effect."""
        return super().satisfaction()


class Orb(BoardTile):

    """Orb item."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Orb
        self.strip_frame = 23

    def satisfaction(self) -> int:
        """Orb cannot be placed near an edge."""
        if is_close_to_edge(self.tx, self.ty):
            return -10000
        return 0


class Treasure(BoardTile):

    """Treasure item."""

    def __init__(self, xp: int = 1) -> None:
        """"""
        super().__init__()
        self.id = TileID.Treasure
        self.xp = xp
        if xp == 1:
            self.strip_frame = 30
        elif xp == 3:
            self.strip_frame = 31
        else:  # xp == 5
            self.strip_frame = 24

    def satisfaction(self) -> int:
        """Treasure has no locational satisfaction effect."""
        return super().satisfaction()
