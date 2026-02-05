"""Module to house the dungeon population and generation logic."""

import copy
import logging
import random

from dragonsweepyr.config import config
from dragonsweepyr.happiness import happiness
from dragonsweepyr.monsters import creatures, items, obstacles, spells
from dragonsweepyr.monsters.tiles import BoardTile, TileID
from dragonsweepyr.utils import distance, res_to_frame

logger = logging.getLogger(__name__)


class Floor:

    """Simple class to store the 2D array of board tiles and a registry of populated tiles."""

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the board with given dimensions.

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
        self.chest_locations: list[tuple[int, int]] = []
        self.wall_locations: list[tuple[int, int]] = []

        self.satisfaction: int = 0

    def __repr__(self) -> str:
        """Display the floor layout (for debugging purposes)."""
        repr_line = ""
        for row in self.tiles:
            for tile in row:
                repr_line += f"{tile.id}|{tile.tx},{tile.ty} "
            repr_line += "\n"
        return repr_line

    def _collect_chest_locations(self) -> None:
        """
        Collect the locations of all chest tiles

        Also set the minotaur chest location property
        """
        chest_tiles = self.get_tile_list(TileID.Chest)
        for chest_tile in chest_tiles:
            self.chest_locations.append((chest_tile.tx, chest_tile.ty))

    def _collect_wall_locations(self) -> None:
        """Collect the locations of all wall tiles."""
        wall_hps = [3, 3, 3, 3, 3, 3]
        wall_hp_counter = 0

        wall_tiles = self.get_tile_list(TileID.Wall)
        for wall_tile in wall_tiles:
            self.wall_locations.append((wall_tile.tx, wall_tile.ty))
            wall_tile.wallHP = wall_tile.wallMaxHP = wall_hps[wall_hp_counter]
            wall_hp_counter = (wall_hp_counter + 1) % len(wall_hps)

    def _fix_tiles(self) -> None:
        """Set all tiles on the floor to fixed."""
        for tile in self.all_tiles():
            tile.fixed = True

    def _swap_tiles(self, tile_a: BoardTile, tile_b: BoardTile) -> None:
        """
        Swap the positions of two tiles on the floor.

        Args:
            tile_a: The first tile to swap.
            tile_b: The second tile to swap.
        """
        self.tiles[tile_a.ty][tile_a.tx], self.tiles[tile_b.ty][tile_b.tx] = self.tiles[tile_b.ty][tile_b.tx], self.tiles[tile_a.ty][tile_a.tx]
        tile_a.tx, tile_b.tx = tile_b.tx, tile_a.tx
        tile_a.ty, tile_b.ty = tile_b.ty, tile_a.ty

    def all_tiles(self) -> list[BoardTile]:
        """
        Get a flat list of all populated tiles in the board.

        Returns:
            A list of all BoardTile instances in the board.
        """
        tile_list: list[BoardTile] = []
        for coord in self.populated:
            tile_list.append(self.tiles[coord[1]][coord[0]])
        return tile_list

    def get_tile_at(self, x: int, y: int) -> BoardTile | None:
        """
        Retrieve a tile at the specified coordinates.

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
        """
        Retrieve the first tile with the specified ID.

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
        """
        Retrieve all tiles with the specified ID.

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
        """
        Mark a tile as populated or unpopulated.

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
        """
        Check if a tile is populated.

        Args:
            x: The x-coordinate (column).
            y: The y-coordinate (row).

        Returns:
            True if the tile is populated, False otherwise.
        """
        return (x, y) in self.populated

    def add_tile(self, tile_class: type[BoardTile] | BoardTile, count: int = 1, **kwargs) -> None:
        """
        Add tile(s) to the floor at random empty positions.

        Args:
            tile_class: The BoardTile class or instance to add.
            count: Number of tiles to add.
            kwargs: Additional properties to set on tiles. Supports any BoardTile attribute, i.e.:
                - monster_level: The monster's level
                - name: Custom name for the tile
                - contains: Item contained in this tile
                - revealed: Whether the tile is revealed

        Returns:
            None
        """
        for _ in range(count):
            # Find all empty positions
            empty_positions = [
                (x, y) for y in range(self.height)
                for x in range(self.width)
                if not self.is_populated(x, y)
            ]

            if not empty_positions:
                break  # No more empty positions

            # Choose random position
            x, y = random.choice(empty_positions)

            # Create tile instance
            if isinstance(tile_class, type):
                tile = tile_class()
            else:
                # If it's already an instance, make a deep copy
                tile = copy.deepcopy(tile_class)

            # Set position
            tile.tx = x
            tile.ty = y

            # Set additional properties from kwargs
            for key, value in kwargs.items():

                if hasattr(tile, key):
                    setattr(tile, key, value)

            # Place tile on the floor
            self.tiles[y][x] = tile
            self.set_populated(x, y, True)

    def post_process_layer(self) -> None:
        """
        Perform any post-processing needed on the floor layer.

        Javascript Source: endLayer()


        for(let a of layerActors)
        {
            a.fixed = true;
        }
        """
        if self.satisfaction == 0:
            self.satisfaction = happiness(self)

        for _ in range(4):
            # Shuffle the order of the tiles to prevent bias in processing
            random.shuffle(self.all_tiles())

            for tile_a in self.all_tiles():
                if tile_a.fixed:
                    continue

                happiest_replacement = None
                best_satisfaction = self.satisfaction

                for tile_b in self.all_tiles():
                    if tile_b.fixed or tile_a == tile_b:
                        continue

                    # Swap tiles and evaluate satisfaction
                    self._swap_tiles(tile_a, tile_b)
                    new_satisfaction = happiness(self)
                    self._swap_tiles(tile_a, tile_b)  # Swap back

                    if new_satisfaction >= best_satisfaction:
                        best_satisfaction = new_satisfaction
                        happiest_replacement = tile_b

                if happiest_replacement:
                    self._swap_tiles(tile_a, happiest_replacement)
                    self.satisfaction = best_satisfaction

        self._fix_tiles()

    def finalize_floor(self) -> None:
        """Perform final setup on the tiles after all layers have been added."""
        self._collect_chest_locations()
        self._collect_wall_locations()

        for tile in self.all_tiles():
            if tile.name == "guard1":
                tile.set_frame(res_to_frame(200, 200))
            elif tile.name == "guard2":
                tile.set_frame(res_to_frame(200, 200) + 1)
            elif tile.name == "guard3":
                tile.set_frame(res_to_frame(200, 200) + 2)
            elif tile.name == "guard4":
                tile.set_frame(res_to_frame(200, 200) + 3)
            elif tile.id == TileID.Minotaur:
                for chest_tile in self.chest_locations:
                    if distance(tile.tx, tile.ty, chest_tile[0], chest_tile[1]) <= 1.5:
                        tile.minotaurChestLocation = [chest_tile[0], chest_tile[1]]
            elif tile.id == TileID.Gargoyle:
                for other_gargoyle in self.get_tile_list(TileID.Gargoyle):
                    if tile != other_gargoyle and other_gargoyle.name == tile.name:
                        if tile.tx < other_gargoyle.tx:
                            tile.set_frame(res_to_frame(0, 210))
                        elif tile.tx > other_gargoyle.tx:
                            tile.set_frame(res_to_frame(0, 210) + 3)
                        elif tile.ty < other_gargoyle.ty:
                            tile.set_frame(res_to_frame(0, 210) + 1)
                        elif tile.ty > other_gargoyle.ty:
                            tile.set_frame(res_to_frame(0, 210) + 2)

    def render_floor(self) -> None:
        """Render the floor tiles to the console (for debugging purposes)."""
        for row in self.tiles:
            row_str = ' '.join(f"{tile.id:02}" for tile in row)
            print(row_str)


class Dungeon:

    """Class representing a dungeon in the game."""

    def __init__(self) -> None:
        """Initialize the dungeon with given configuration."""
        self.buttons: dict[int, int] = {}
        self.dungeon_floor: Floor = Floor(config.grid_columns, config.grid_rows)

        self.set_buttons()

    def __repr__(self) -> str:
        """Display the dungeon layout (for debugging purposes)."""
        repr_line = ""
        for button, tile in zip(self.buttons.items(), self.dungeon_floor.all_tiles()):
            repr_line += f"{tile.id}|{tile.tx},{tile.ty}|{button[1]}"
        return repr_line

    def populate_dungeon(self) -> None:
        """Populate the dungeon with monsters, traps, and items."""
        raise NotImplementedError("Dungeon population logic not yet implemented.")

    def set_buttons(self) -> None:
        """
        Set the button array for the dungeon.

        Buttons represent the covered tile, with the value representing the
        sprite index for the weathering pattern.
        """
        grid_columns = config.grid_columns
        grid_rows = config.grid_rows
        button_sprite_min: int = 4
        button_sprite_max: int = 24

        for y in range(grid_rows):
            for x in range(grid_columns):

                if (x == 0 and y == 0):
                    self.buttons[x + y * grid_columns] = 25  # Top-left corner decor
                elif (x == grid_columns - 1 and y == 0):
                    self.buttons[x + y * grid_columns] = 26  # Top-right corner decor
                else:
                    self.buttons[x + y * grid_columns] = random.randint(button_sprite_min, button_sprite_max)


def generate_dungeon() -> Dungeon:
    """
    Generate and return a new dungeon instance.

    Returns:
        A Dungeon instance with generated layout.
    """
    dungeon = Dungeon()

    # Dungeon is generated in several distinct passes (i.e. layers)
    # 1. Base layer, Dragon and Wizard
    current_floor = dungeon.dungeon_floor
    current_floor.add_tile(creatures.Dragon, revealed=True)
    current_floor.add_tile(creatures.Wizard)
    current_floor.post_process_layer()

    # 2. Big slimes
    current_floor.add_tile(creatures.BigSlime, count=5, monster_level=8)
    current_floor.post_process_layer()

    # 3. Mine King
    current_floor.add_tile(creatures.MineKing)
    current_floor.post_process_layer()

    # 4. Giants (Romeo and Juliet)
    current_floor.add_tile(creatures.Giant, count=1, monster_level=9, name="romeo")
    current_floor.add_tile(creatures.Giant, count=1, monster_level=9, name="juliet")
    # add(2, makeRat1).forEach(a => a.name = "rat_guard");
    current_floor.post_process_layer()

    # 5. Rat King, Walls, Minutours, Guards, Gargoyles, Gazers, Mines, and Items
    current_floor.add_tile(creatures.RatKing)
    current_floor.add_tile(obstacles.Wall, count=6, contains=items.Treasure(1))
    current_floor.add_tile(creatures.Minotaur, count=5, monster_level=6)
    current_floor.add_tile(creatures.Guard, count=1, monster_level=7, name="guard1")
    current_floor.add_tile(creatures.Guard, count=1, monster_level=7, name="guard2")
    current_floor.add_tile(creatures.Guard, count=1, monster_level=7, name="guard3")
    current_floor.add_tile(creatures.Guard, count=1, monster_level=7, name="guard4")
    current_floor.add_tile(creatures.Gargoyle, count=2, monster_level=4, name="gargoyle1")
    current_floor.add_tile(creatures.Gargoyle, count=2, monster_level=4, name="gargoyle2")
    current_floor.add_tile(creatures.Gargoyle, count=2, monster_level=4, name="gargoyle3")
    current_floor.add_tile(creatures.Gargoyle, count=2, monster_level=4, name="gargoyle4")
    current_floor.add_tile(creatures.Gazer, count=2)
    current_floor.add_tile(creatures.Mine, count=9)
    # add( 1, makeMine).forEach(a => a.name = "mine_with_orb");
    # add( 3, makeWall).forEach(a => a.contains = makeTreasure1);
    current_floor.add_tile(items.Medikit, count=5)
    current_floor.add_tile(items.Chest, count=3)
    # add( 1, makeChest).forEach(a => a.contains = makeSpellOrb);
    current_floor.add_tile(items.Chest, count=2, contains=items.Medikit)
    # add(1, makeOrb).forEach(a => a.revealed = true);
    current_floor.add_tile(items.Orb, count=1, revealed=True, name="orb_with_healing")
    # add(2, makeMedikit); .forEach(a => a.revealed = true);
    # add(1, makeFidel);
    current_floor.add_tile(creatures.DragonEgg, count=1)
    current_floor.post_process_layer()

    # 6. Common monsters (Rats, Bats, Skeletons oh my!)
    current_floor.add_tile(creatures.Rat, count=13, monster_level=1)
    current_floor.add_tile(creatures.Bat, count=12, monster_level=2)
    current_floor.add_tile(creatures.Skeleton, count=10, monster_level=3)
    current_floor.add_tile(creatures.Slime, count=8, monster_level=5)
    current_floor.add_tile(creatures.Mimic, count=1)
    current_floor.add_tile(creatures.Gnome, count=1)
    current_floor.add_tile(spells.SpellMakeOrb, count=1)
    current_floor.post_process_layer()

    current_floor.finalize_floor()  # Perform any final adjustments to the floor after all layers are added

    """Javascript source:
    computeStats()
    if(!RELEASE)
    {
        checkLevel();
    }
    """

    return dungeon
