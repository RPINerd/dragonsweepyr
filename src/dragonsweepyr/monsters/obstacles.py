"""Small module to house the decoration and wall tiles."""
from dragonsweepyr.monsters.tiles import BoardTile, TileID


class Decoration(BoardTile):

    """Decoration tile."""

    def __init__(self, strip=None, frame: int = 0) -> None:
        """"""
        super().__init__()
        self.id = TileID.Decoration
        self.strip = strip
        self.stripFrame = frame


class Wall(BoardTile):

    """Wall tile."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Wall
        self.stripFrame = 11

    def satisfaction(self) -> int:
        """
        Currently walls do not contribute to satisfaction.

        Source code does have commented out logic to discourage walls from being along the board edges.
        """
        # if is_edge(self.tx, self.ty):
        #     return -1000
        return super().satisfaction()
