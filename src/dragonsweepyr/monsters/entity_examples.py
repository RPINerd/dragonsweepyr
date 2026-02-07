"""Example usage patterns for the data-driven entity system."""

# ============================================================================
# EXAMPLE 1: Basic Entity Creation
# ============================================================================

from dragonsweepyr.monsters import TileID, entity_factory

# Create an entity by ID
bat = entity_factory.create(TileID.Bat)
print(f"Created {bat.name} at sprite frame {bat.strip_frame}")

# Create an entity by name
dragon = entity_factory.create_by_name("Dragon")
print(f"Dragon has {dragon.xp} xp")


# ============================================================================
# EXAMPLE 2: Batch Creation and Sprite Updates
# ============================================================================

from dragonsweepyr.monsters import ENTITY_REGISTRY

# Create multiple entities of different types
entities = []
for entity_id in [TileID.Rat, TileID.Slime, TileID.Treasure]:
    tile = entity_factory.create(entity_id)
    entities.append(tile)

# Update all sprites easily (e.g., for scaling)
for tile in entities:
    # Access sprite frame data
    print(f"{tile.name}: frame={tile.strip_frame}")


# ============================================================================
# EXAMPLE 3: Rendering with Unified Sprite System
# ============================================================================

def render_board(board):
    """Render all tiles as sprites."""
    sprites = []

    for row in board:
        for tile in row:
            # All tiles are pygame.sprite.Sprite subclasses
            if tile.strip_frame > 0:  # Skip empty tiles
                # Get sprite image from spritesheet
                image = get_sprite_image(tile.strip)
                rect = image.get_rect()
                rect.center = (tile.tx * 16, tile.ty * 16)
                sprites.append((image, rect))

    return sprites


# ============================================================================
# EXAMPLE 4: Dynamic Entity Creation Based on Level
# ============================================================================

def spawn_monster_for_level(level: int):
    """Spawn appropriate monster for dungeon level."""
    # Map levels to entity IDs
    level_entities = {
        1: TileID.Rat,
        2: TileID.Bat,
        3: TileID.Skeleton,
        4: TileID.Gargoyle,
        5: TileID.Eye,
        # ... more levels
    }

    entity_id = level_entities.get(level, TileID.Rat)
    monster = entity_factory.create(entity_id)
    monster.monster_level = level
    monster.xp = level
    return monster


# ============================================================================
# EXAMPLE 5: Satisfying Placement Rules
# ============================================================================

def place_dragon(board, satisfaction_threshold=5000):
    """Place dragon considering its satisfaction function."""
    dragon = entity_factory.create(TileID.Dragon)

    best_pos = None
    best_satisfaction = -float('inf')

    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y].id == TileID.Empty:
                # Temporarily place to evaluate
                dragon.tx, dragon.ty = x, y
                satisfaction = dragon.satisfaction()

                if satisfaction > best_satisfaction:
                    best_satisfaction = satisfaction
                    best_pos = (x, y)

    if best_pos and best_satisfaction >= satisfaction_threshold:
        dragon.tx, dragon.ty = best_pos
        return dragon

    return None


# ============================================================================
# EXAMPLE 6: Registry Iteration and Filtering
# ============================================================================

# Get all monster entities
monsters = [
    entity_factory.create(entity_id)
    for entity_id, definition in ENTITY_REGISTRY.items()
    if definition.is_monster
]

# Get all items
items = [
    entity_factory.create(entity_id)
    for entity_id, definition in ENTITY_REGISTRY.items()
    if not definition.is_monster and entity_id not in [TileID.Wall, TileID.Decoration]
]

# Get high-level creatures
high_level = [
    entity_factory.create(entity_id)
    for entity_id, definition in ENTITY_REGISTRY.items()
    if definition.monster_level >= 8
]


# ============================================================================
# EXAMPLE 7: Accessing Entity Metadata
# ============================================================================

# Get entity definition to access raw data
definition = entity_factory.get_definition(TileID.Guard)

print(f"Name: {definition.name}")
print(f"Sprite frame: {definition.sprite_frame}")
print(f"Is monster: {definition.is_monster}")
print(f"Monster level: {definition.monster_level}")
print(f"XP value: {definition.xp}")
print(f"Metadata: {definition.metadata}")


# ============================================================================
# EXAMPLE 8: Custom Entity Variants
# ============================================================================

def create_treasure_hoard(count: int):
    """Create a treasure hoard with increasing XP."""
    treasures = []
    xp_values = [1, 3, 5, 1, 3, 5]  # Cycling pattern

    for i in range(count):
        treasure = entity_factory.create(TileID.Treasure)
        xp = xp_values[i % len(xp_values)]
        treasure.xp = xp

        # Update sprite based on xp (matches original logic)
        if xp == 1:
            treasure.strip_frame = 30
        elif xp == 3:
            treasure.strip_frame = 31
        else:  # xp == 5
            treasure.strip_frame = 24

        treasures.append(treasure)

    return treasures


# ============================================================================
# EXAMPLE 9: Backward Compatible Legacy Code
# ============================================================================

# Original imports still work
from dragonsweepyr.monsters.creatures import Bat, Dragon, Wizard
from dragonsweepyr.monsters.items import Chest, Treasure
from dragonsweepyr.monsters.obstacles import Wall

# These function calls work exactly as before
bat = Bat(monster_level=2)
dragon = Dragon(monster_level=13)
wizard = Wizard(monster_level=1)
chest = Chest(contains=Treasure(5))
wall = Wall()

# But internally they use entity_factory
assert bat.id == TileID.Bat
assert dragon.satisfaction() >= 0  # Can now use satisfaction functions


# ============================================================================
# EXAMPLE 10: Batch Update Sprite Frames from JSON
# ============================================================================


def reload_sprite_frames_from_json(json_path):
    """Update all entity sprite frames from a JSON file."""
    from dragonsweepyr.monsters.entity_definitions import _load_sprite_coords

    # Reload sprite coordinates
    coords = _load_sprite_coords()

    # Update registry (would need modification to entity_definitions.py)
    # This shows the advantage of data-driven design - easy to refresh
    # without reloading modules

    return coords
