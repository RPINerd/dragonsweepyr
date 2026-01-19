"""Module to house the dungeon population and generation logic."""


from dragonsweepyr.config import config
from dragonsweepyr.dragons import BoardTile
from random import randint


class Dungeon:

    """Class representing a dungeon in the game."""

    def __init__(self) -> None:
        """Initialize the dungeon with given configuration."""
        self.buttons: dict[int, int] = {}
        self.tiles: list[BoardTile] = []

    def __repr__(self) -> str:
        """Display the dungeon layout (for debugging purposes)."""
        repr_line = ""
        for button, tile in zip(self.buttons.items(), self.tiles):
            repr_line += f"{tile.id}|{tile.tx},{tile.ty}|{button[1]}"
        return repr_line

    def populate_dungeon(self, tile_array: list[BoardTile]) -> None:
        """Populate the dungeon with monsters, traps, and items."""
        self.tiles = tile_array

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
    tile_array: list[BoardTile] = []
    for y in range(grid_rows):
        for x in range(grid_columns):
            new_tile = BoardTile()
            new_tile.tx = x
            new_tile.ty = y
            tile_array.append(new_tile)

            if (x == 0 and y == 0):
                button_array[x + y * grid_columns] = 25  # Top-left corner decor
            elif (x == grid_columns - 1 and y == 0):
                button_array[x + y * grid_columns] = 26  # Top-right corner decor
            else:
                button_array[x + y * grid_columns] = randint(button_sprite_min, button_sprite_max)

    dungeon.set_buttons(button_array)

    # Dungeon is generated in several distinct passes (i.e. layers)
    # 1. Base layer, Dragon and Wizard
    add(1, makeDragon);
    add(1, makeWizard);
    post_process_layer()

    # 2. Big slimes
    add(5, makeBigSlime8);
    post_process_layer()

    # 3. Mine King
    add(1, makeMineKing);
    post_process_layer()

    # 4. Giants (Romeo and Juliet)
    add( 1, makeGiant9).forEach(a => a.name = "romeo");
    add( 1, makeGiant9).forEach(a => a.name = "juliet");
    # add(2, makeRat1).forEach(a => a.name = "rat_guard");
    post_process_layer()

    # 5. Rat King, Walls, Minutours, Guards, Gargoyles, Gazers, Mines, and Items
    add(1, makeRatKing);
    add( 6, makeWall).forEach(a => a.contains = makeTreasure1);
    add( 5, makeMinotaur6);
    add( 1, makeGuard7).forEach(a => a.name = "guard1");
    add( 1, makeGuard7).forEach(a => a.name = "guard2");
    add( 1, makeGuard7).forEach(a => a.name = "guard3");
    add( 1, makeGuard7).forEach(a => a.name = "guard4");
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle1");
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle2");
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle3");
    add( 2, makeGargoyle4).forEach(a => a.name = "gargoyle4");
    add( 2, makeGazer);
    add( 9, makeMine);
    #add( 1, makeMine).forEach(a => a.name = "mine_with_orb");
    #add( 3, makeWall).forEach(a => a.contains = makeTreasure1);
    add( 5, makeMedikit);
    add( 3, makeChest);
    #add( 1, makeChest).forEach(a => a.contains = makeSpellOrb);
    add( 2, makeChest).forEach(a => a.contains = makeMedikit);
    #add(1, makeOrb).forEach(a => a.revealed = true);
    add(1, makeOrb).forEach(a => {a.revealed = true; a.name = "orb_with_healing";});
    #add(2, makeMedikit); .forEach(a => a.revealed = true);
    #add(1, makeFidel);
    add(1, makeDragonEgg);
    post_process_layer()

    # 6. Common monsters (Rats, Bats, Skeletons oh my!)
    add(13, makeRat1);
    add(12, makeBat2);
    add(10, makeSkeleton3);
    add( 8, makeSlime5);
    add( 1, makeMimic);
    add(1, makeGnome);
    add( 1, makeSpellOrb);
    post_process_layer()

    return dungeon

def post_process_layer() -> None:
    """Perform any post-processing needed on the dungeon layer."""
    pass