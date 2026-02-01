"""Module to house the dungeon population and generation logic."""


from dragonsweepyr.config import config
from dragonsweepyr.monsters.tiles import BoardTile
from random import randint

from dragonsweepyr.utils import distance


class Floor:

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

    def all_tiles(self) -> list[BoardTile]:
        """Get a flat list of all tiles in the board.

        Returns:
            A list of all BoardTile instances in the board.
        """
        return [tile for row in self.tiles for tile in row]

    def get_tile_at(self, x: int, y: int) -> BoardTile | None:
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

    def get_tile_id(self, tile_id: int) -> BoardTile | None:
        """Retrieve the first tile with the specified ID.

        Args:
            tile_id: The ID of the tile to find.

        Returns:
            The first BoardTile with the specified ID, or None if not found.
        """
        for row in self.tiles:
            for tile in row:
                if tile.id == tile_id:
                    return tile
        return None

    def get_tiles_in_radius(self, center_x: int, center_y: int, radius: int | float) -> list[BoardTile]:
        """
        Retrieve all tiles within a certain radius from a center point.

        Ingnores the center (self) tile.

        Args:
            center_x: The x-coordinate (column) of the center point.
            center_y: The y-coordinate (row) of the center point.
            radius: The radius within which to find tiles.

        Returns:
            A list of BoardTile instances within the specified radius.
        """
        found_tiles: list[BoardTile] = []
        for row in self.tiles:
            for tile in row:
                if tile.tx == center_x and tile.ty == center_y:
                    continue  # Skip the center tile itself
                if distance(tile.tx, tile.ty, center_x, center_y) <= radius:
                    found_tiles.append(tile)
        return found_tiles

    def get_tile_list(self, tile_id: int) -> list[BoardTile]:
        """Retrieve all tiles with the specified ID.

        Args:
            tile_id: The ID of the tiles to find.

        Returns:
            A list of BoardTile instances with the specified ID.
        """
        found_tiles: list[BoardTile] = []
        for row in self.tiles:
            for tile in row:
                if tile.id == tile_id:
                    found_tiles.append(tile)
        return found_tiles

    def count_identical_neighbors(self, target_tile: BoardTile, radius: int) -> int:
        """
        Count the number of identical neighboring tiles within a given radius.

        Javascript Source: countNearMeWithSameId(a, minDistance)

        Args:
            target_tile: The tile to check neighbors for.
            radius: The radius within which to count identical neighbors.

        Returns:
            The count of identical neighboring tiles.
        """
        count = 0
        for y in range(max(0, target_tile.ty - radius), min(self.height, target_tile.ty + radius + 1)):
            for x in range(max(0, target_tile.tx - radius), min(self.width, target_tile.tx + radius + 1)):
                if (x, y) != (target_tile.tx, target_tile.ty):
                    neighbor_tile = self.get_tile_at(x, y)
                    if neighbor_tile and neighbor_tile.id == target_tile.id:
                        count += 1
        return count

    def count_within_distance(self, source_pos: tuple[int, int], target_id: int, max_distance: float) -> int:
        """
        Count the number of tiles with the specified ID within a certain distance from a given position.

        Args:
            source_pos: The (tx, ty) position to check from.
            target_id: The TileID to search for.
            max_distance: The maximum distance to consider.

        Returns:
            The count of tiles with the target ID within the specified distance.
        """
        count = 0
        source_tx, source_ty = source_pos
        for tile in self.all_tiles():
            if tile.id != target_id:
                continue

            if distance(source_tx, source_ty, tile.tx, tile.ty) <= max_distance:
                count += 1
        return count

    def is_within_distance(self, tile_a: BoardTile, target_id: int, max_distance: float) -> bool:
        """
        Check if there is a tile with the specified ID within a certain distance from the given tile.

        Javascript Source: isNearId(a, actorId, dist)

        Args:
            tile_a: The reference tile.
            target_id: The TileID to search for.
            max_distance: The maximum distance to consider.

        Returns:
            True if a tile with the target ID is within the specified distance, False otherwise.
        """
        for tile_b in self.all_tiles():
            if tile_b.id != target_id:
                continue
            if distance(tile_a.tx, tile_a.ty, tile_b.tx, tile_b.ty) <= max_distance:
                return True
        return False

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
        self.dungeon_floor: Floor = Floor(config.grid_columns, config.grid_rows)

    def __repr__(self) -> str:
        """Display the dungeon layout (for debugging purposes)."""
        repr_line = ""
        for button, tile in zip(self.buttons.items(), self.dungeon_floor.all_tiles()):
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

    let layerActors = [];
        for(let layerActorToAdd of currentLayer.actors)
        {
            let availableActor = state.actors.find(a => isEmpty(a));
            if(availableActor == undefined) continue;
            availableActor.copyFrom(layerActorToAdd);
            layerActors.push(availableActor);
        }

        let bestHappiness = happiness();
        for(let k = 0; k < 4; k++)
        {
            shuffle(state.actors);
            for(let i = 0; i < layerActors.length; i++)
            {
                let a = layerActors[i];
                let happiestReplacement = null;
                for(let j = 0; j < state.actors.length; j++)
                {
                    let b = state.actors[j];
                    if(b.fixed || a === b) continue;
                    swapPlaces(a, b);
                    let newHappiness = happiness();
                    swapPlaces(a, b);
                    if(newHappiness >= bestHappiness)
                    {
                        bestHappiness = newHappiness;
                        happiestReplacement = b;
                    }
                }

                if(happiestReplacement != null)
                {
                    swapPlaces(a, happiestReplacement);
                }
            }
        }

        for(let a of layerActors)
        {
            a.fixed = true;
        }
    """
    raise NotImplementedError("Dungeon layer post-processing not yet implemented.")


def swap_tiles(a: BoardTile, b: BoardTile) -> None:
    """
    Swap the positions of two tiles.

    Javascript Source: swapPlaces(a, b)

    Args:
        a: The first tile to swap.
        b: The second tile to swap.
    """
    a.tx, b.tx = b.tx, a.tx
    a.ty, b.ty = b.ty, a.ty
