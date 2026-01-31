"""Module to house the dungeon population and generation logic."""


from dragonsweepyr.config import config
from dragonsweepyr.dragons import BoardTile
from random import randint


class Board:

    """Simple class to store the 2D array of board tiles and a registry of populated tiles."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize the board with given dimensions.

        Args:
            width: The number of columns in the board.
            height: The number of rows in the board.
        """
        self.width = width
        self.height = height
        self.tiles: list[list[BoardTile]] = [
            [BoardTile() for _ in range(width)] for _ in range(height)
        ]
        self.populated: set[tuple[int, int]] = set()

    def get_tile(self, x: int, y: int) -> BoardTile | None:
        """Retrieve a tile at the specified coordinates.

        Args:
            x: The x-coordinate (column).
            y: The y-coordinate (row).

        Returns:
            The BoardTile at the specified position, or None if out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def all_tiles(self) -> list[BoardTile]:
        """Get a flat list of all tiles in the board.

        Returns:
            A list of all BoardTile instances in the board.
        """
        return [tile for row in self.tiles for tile in row]

    def set_populated(self, x: int, y: int, is_populated: bool) -> None:
        """Mark a tile as populated or unpopulated.

        Args:
            x: The x-coordinate (column).
            y: The y-coordinate (row).
            is_populated: Whether the tile should be marked as populated.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            if is_populated:
                self.populated.add((x, y))
            else:
                self.populated.discard((x, y))

    def is_populated(self, x: int, y: int) -> bool:
        """Check if a tile is populated.

        Args:
            x: The x-coordinate (column).
            y: The y-coordinate (row).

        Returns:
            True if the tile is populated, False otherwise.
        """
        return (x, y) in self.populated


class Dungeon:

    """Class representing a dungeon in the game."""

    def __init__(self) -> None:
        """Initialize the dungeon with given configuration."""
        self.buttons: dict[int, int] = {}
        self.gameboard: Board = Board(config.grid_columns, config.grid_rows)

    def __repr__(self) -> str:
        """Display the dungeon layout (for debugging purposes)."""
        repr_line = ""
        for button, tile in zip(self.buttons.items(), self.gameboard.all_tiles()):
            repr_line += f"{tile.id}|{tile.tx},{tile.ty}|{button[1]}"
        return repr_line

    def populate_dungeon(self) -> None:
        """Populate the dungeon with monsters, traps, and items."""
        raise NotImplementedError("Dungeon population logic not yet implemented.")

    def set_buttons(self, button_array: dict[int, int]) -> None:
        """Set the button array for the dungeon."""
        self.buttons = button_array


def generate_dungeon() -> Dungeon:
    """
    Generate and return a new dungeon instance.

    Returns:
        A Dungeon instance with generated layout.
    """
    dungeon = Dungeon()
    grid_columns = config.grid_columns
    grid_rows = config.grid_rows

    # Buttons represent the covered tile, with the value representing the sprite index for
    # the weathering pattern.
    # Tiles represent the actual tile underneath the button; monsters, traps, empty, etc.
    button_sprite_min: int = 4
    button_sprite_max: int = 24
    button_array: dict[int, int] = {}
    # tile_array: list[BoardTile] = []
    for y in range(grid_rows):
        for x in range(grid_columns):
            # new_tile = BoardTile()
            # new_tile.tx = x
            # new_tile.ty = y
            # tile_array.append(new_tile)

            if (x == 0 and y == 0):
                button_array[x + y * grid_columns] = 25  # Top-left corner decor
            elif (x == grid_columns - 1 and y == 0):
                button_array[x + y * grid_columns] = 26  # Top-right corner decor
            else:
                button_array[x + y * grid_columns] = randint(button_sprite_min, button_sprite_max)

    dungeon.set_buttons(button_array)

    # Dungeon is generated in several distinct passes (i.e. layers)
    # 1. Base layer, Dragon and Wizard
    add(1, makeDragon)
    add(1, makeWizard)
    post_process_layer()

    # 2. Big slimes
    add(5, makeBigSlime8)
    post_process_layer()

    # 3. Mine King
    add(1, makeMineKing)
    post_process_layer()

    # 4. Giants (Romeo and Juliet)
    add( 1, makeGiant9).forEach(a => a.name = "romeo")
    add( 1, makeGiant9).forEach(a => a.name = "juliet")
    # add(2, makeRat1).forEach(a => a.name = "rat_guard");
    post_process_layer()

    # 5. Rat King, Walls, Minutours, Guards, Gargoyles, Gazers, Mines, and Items
    add(1, makeRatKing)
    add( 6, makeWall).forEach(a => a.contains = makeTreasure1)
    add( 5, makeMinotaur6)
    add( 1, makeGuard7).forEach(a => a.name = "guard1")
    add( 1, makeGuard7).forEach(a => a.name = "guard2")
    add( 1, makeGuard7).forEach(a => a.name = "guard3")
    add( 1, makeGuard7).forEach(a => a.name = "guard4")
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle1")
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle2")
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle3")
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle4")
    add( 2, makeGazer)
    add( 9, makeMine)
    #add( 1, makeMine).forEach(a => a.name = "mine_with_orb");
    #add( 3, makeWall).forEach(a => a.contains = makeTreasure1);
    add( 5, makeMedikit)
    add( 3, makeChest)
    #add( 1, makeChest).forEach(a => a.contains = makeSpellOrb);
    add( 2, makeChest).forEach(a => a.contains = makeMedikit)
    #add(1, makeOrb).forEach(a => a.revealed = true);
    add(1, makeOrb).forEach(a => {a.revealed = true; a.name = "orb_with_healing";})
    #add(2, makeMedikit); .forEach(a => a.revealed = true);
    #add(1, makeFidel);
    add(1, makeDragonEgg)
    post_process_layer()

    # 6. Common monsters (Rats, Bats, Skeletons oh my!)
    add(13, makeRat1)
    add(12, makeBat2)
    add(10, makeSkeleton3)
    add( 8, makeSlime5)
    add( 1, makeMimic)
    add(1, makeGnome)
    add( 1, makeSpellOrb)
    post_process_layer()

    return dungeon


def post_process_layer() -> None:
    """
    Perform any post-processing needed on the dungeon layer.

    Javascript Source: endLayer()
    """

    pass