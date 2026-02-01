"""Module to calculate the happiness score of the current dungeon state."""
import logging

from dragonsweepyr.config import config
from dragonsweepyr.const import ORB_RADIUS
from dragonsweepyr.dungeon import Board
from dragonsweepyr.monsters.tiles import BoardTile, TileID
from dragonsweepyr.utils import distance, is_edge

logger = logging.getLogger(__name__)


def happiness(current_board: Board) -> int:
    """
    Calculate the happiness score of the current dungeon state.

    TODO could probably move all happiness logic for specific monsters/items into their respective classes and simply pass the current board

    Javascript Source: happiness()
    """
    happiness_score = 0

    for tile in current_board.all_tiles():
        # Individual tiles can have satisfaction based on their absolute position on the board
        happiness_score += tile.satisfaction()

        # Additional happiness logic based on specific monster/item placements
        match tile.id:

            case TileID.BigSlime:
                wizard_tile = current_board.get_tile(TileID.Wizard)
                if not wizard_tile:
                    logger.warning("BigSlime could not find a Wizard tile.")
                    continue
                happiness_score += 1000 if tile.is_near(wizard_tile, 1.5) else 0

            case TileID.DragonEgg:
                dragon_tile = current_board.get_tile(TileID.Dragon)
                if not dragon_tile:
                    logger.warning("DragonEgg could not find a Dragon tile.")
                    continue
                happiness_score += 9000 if tile.is_near(dragon_tile, 1.5) else 0

            case TileID.Fidel:
            #     chest_tiles = current_board.get_tile_list(TileID.Chest)
            #     if not chest_tiles:
            #         logger.warning("Fidel could not find any Chest tiles.")
            #         continue
            #     if not any(tile.is_near(chest_tile, 1.5) for chest_tile in chest_tiles):
            #         happiness_score += 9000
                pass

            case TileID.Gargoyle:
                current_gargoyles = current_board.get_tile_list(TileID.Gargoyle)
                for potential_twin in current_gargoyles:
                    if tile == potential_twin:
                        continue
                    if tile.name == potential_twin.name:
                        happiness_score += 1000 if tile.is_near(potential_twin, 1.5) else 0
                        break

            case TileID.Giant:
                center_x = config.grid_columns / 2
                all_giants = current_board.get_tile_list(TileID.Giant)
                my_love = None
                for giant in all_giants:
                    if giant != tile:
                        my_love = giant
                        break

                if not my_love:
                    logger.warning("Giant could not find its love.")
                    continue

                # Romeo should be on the left side, Juliet on the right
                if (tile.name == "romeo" and tile.tx <= 5) or (tile.name == "juliet" and tile.tx >= 7):
                    happiness_score += 1000

                # Check if the lovers are symmetrically placed across the center
                if tile.ty == my_love.ty and abs(tile.tx - center_x) == abs(my_love.tx - center_x):
                    happiness_score += 10000

            case TileID.Gnome:
                medkit_tiles = current_board.get_tile_list(TileID.Medikit)
                if not medkit_tiles:
                    logger.warning("Gnome could not find any Medikit tiles.")
                    continue
                if any(tile.is_near(medkit_tile, 1.5) for medkit_tile in medkit_tiles):
                    happiness_score += 10000

                # Gnome also has a commented out condition in the original JS
                # target_tile = get_favorite_jump_target(current_board, tile)
                # if target_tile and target_tile.tx == tile.tx and target_tile.ty == tile.ty:
                #     happiness_score += 5000

            case TileID.Minotaur:
                # Minotaur wants to be within 2 tiles of a Chest but not within 2 tiles of another Minotaur
                other_minotaurs = [m for m in current_board.get_tile_list(TileID.Minotaur) if m != tile]
                if not other_minotaurs:
                    logger.info("Only one Minotaur present; skipping proximity check.")
                elif any(tile.is_near(minotaur, 2) for minotaur in other_minotaurs):
                    continue

                chest_tiles = current_board.get_tile_list(TileID.Chest)
                if not chest_tiles:
                    logger.warning("Minotaur could not find any Chest tiles.")
                    continue
                nearby_chest_count = sum(1 for chest_tile in chest_tiles if tile.is_near(chest_tile, 2))
                if nearby_chest_count == 1:
                    happiness_score += 10000

            case TileID.Rat:
                if not tile.name.endswith("_guard"):
                    continue

                rat_king_tile = current_board.get_tile(TileID.RatKing)
                if not rat_king_tile:
                    logger.warning("Rat could not find a RatKing tile.")
                    continue
                if tile.is_near(rat_king_tile, 1) and tile.ty == rat_king_tile.ty:
                    happiness_score += 1000

            case TileID.Chest:
                happiness_score -= 1000 * count_identical_neighbors(current_board, tile, 3)

            case TileID.Medikit:
                # TODO current function cannot use float values, in JS source value is 3.5
                happiness_score -= 1000 * count_identical_neighbors(current_board, tile, 4)

            case TileID.Wall:
                close_count = 0
                far_count = 0
                on_edge = 1 if is_edge(tile.tx, tile.ty) else 0

                for neighbor in current_board.all_tiles():
                    if neighbor is tile:
                        continue
                    if neighbor.id != TileID.Wall:
                        continue
                    if on_edge >= 2:
                        break
                    if far_count > 0:
                        break
                    if close_count > 1:
                        break

                    dist = distance(tile.tx, tile.ty, neighbor.tx, neighbor.ty)
                    if dist <= 1:
                        close_count += 1
                        if is_edge(neighbor.tx, neighbor.ty):
                            on_edge += 1
                    elif dist < 1.5:
                        far_count += 1

                happiness_score += 2000

            case TileID.Orb:
                # The orb has complicated happiness logic, factored out into its own method
                happiness_score += orb_happiness(tile, current_board)

            case _:
                pass

    return happiness_score


def count_identical_neighbors(board: Board, target_tile: BoardTile, radius: int) -> int:
    """
    Count the number of identical neighboring tiles within a given radius.

    Javascript Source: countNearMeWithSameId(a, minDistance)

    Args:
        board: The current dungeon board.
        target_tile: The tile to check neighbors for.
        radius: The radius within which to count identical neighbors.

    Returns:
        The count of identical neighboring tiles.
    """
    count = 0
    for y in range(max(0, target_tile.ty - radius), min(board.height, target_tile.ty + radius + 1)):
        for x in range(max(0, target_tile.tx - radius), min(board.width, target_tile.tx + radius + 1)):
            if (x, y) != (target_tile.tx, target_tile.ty):
                neighbor_tile = board.get_tile_at(x, y)
                if neighbor_tile and neighbor_tile.id == target_tile.id:
                    count += 1
    return count


def count_within_distance(board: Board, source_pos: tuple[int, int], target_id: int, max_distance: float) -> int:
    """
    Count the number of tiles with the specified ID within a certain distance from a given position.

    Args:
        board: The current dungeon board.
        source_pos: The (tx, ty) position to check from.
        target_id: The TileID to search for.
        max_distance: The maximum distance to consider.

    Returns:
        The count of tiles with the target ID within the specified distance.
    """
    count = 0
    source_tx, source_ty = source_pos
    for tile in board.all_tiles():
        if tile.id != target_id:
            continue

        if distance(source_tx, source_ty, tile.tx, tile.ty) <= max_distance:
            count += 1
    return count


def is_within_distance(board: Board, tile_a: BoardTile, target_id: TileID, max_distance: float) -> bool:
    """
    Check if there is a tile with the specified ID within a certain distance from the given tile.

    Javascript Source: isNearId(a, actorId, dist)

    Args:
        board: The current dungeon board.
        tile_a: The reference tile.
        target_id: The TileID to search for.
        max_distance: The maximum distance to consider.

    Returns:
        True if a tile with the target ID is within the specified distance, False otherwise.
    """
    for tile_b in board.all_tiles():
        if tile_b.id != target_id:
            continue
        if distance(tile_a.tx, tile_a.ty, tile_b.tx, tile_b.ty) <= max_distance:
            return True
    return False


def orb_happiness(orb: BoardTile, board: Board) -> int:
    """
    Calculate the satisfaction score for the Orb tile based on its position and neighbors.

    Args:
        board (Board): The current dungeon board.

    Returns:
        int: The satisfaction score for the Orb tile.
    """
    forbidden_reveals = {
        TileID.Dragon,
        TileID.Gazer,
        TileID.Chest,
        TileID.SpellMakeOrb,
        TileID.RatKing,
        TileID.Mine,
        TileID.Fidel,
        TileID.DragonEgg,
        TileID.BigSlime,
        TileID.Mimic,
        }
    satisfaction = 0

    # mines_in_range = count_within_distance(board, (orb.tx, orb.ty), TileID.Mine, ORB_RADIUS)
    medikits_in_range = count_within_distance(board, (orb.tx, orb.ty), TileID.Medikit, ORB_RADIUS)
    walls_in_range = count_within_distance(board, (orb.tx, orb.ty), TileID.Wall, ORB_RADIUS)
    if medikits_in_range == 1 and walls_in_range > 0:
        satisfaction += 2000
    if walls_in_range > 2:
        satisfaction += (walls_in_range - 2) * -2000

    for tile in board.get_tiles_in_radius(orb.tx, orb.ty, ORB_RADIUS):
        if tile.id in forbidden_reveals:
            satisfaction += -2000

    return satisfaction
