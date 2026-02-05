"""Small module to house the decoration and wall tiles."""
from dragonsweepyr.monsters.tiles import BoardTile, TileID


class Decoration(BoardTile):

    """Decoration tile."""

    def __init__(self, strip=None, frame: int = 0) -> None:
        """"""
        super().__init__()
        self.id = TileID.Decoration
        self.strip = strip
        self.strip_frame = frame


class Wall(BoardTile):

    """Wall tile."""

    def __init__(self, contains: BoardTile | None = None) -> None:
        """"""
        super().__init__()
        self.id = TileID.Wall
        self.strip_frame = 11
        self.contains = contains

    def satisfaction(self) -> int:
        """
        Currently walls do not contribute to satisfaction.

        Source code does have commented out logic to discourage walls from being along the board edges.
        """
        # if is_edge(self.tx, self.ty):
        #     return -1000
        return super().satisfaction()
