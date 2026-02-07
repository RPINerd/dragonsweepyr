# Data-Driven Entity System Migration

## Overview

The monster/entity system has been refactored to use a **data-driven architecture** instead of individual class definitions. This provides better organization, easier sprite management, and simpler rendering updates.

## Key Changes

### 1. **New Module: `entity_definitions.py`**
   - Contains all entity data definitions in a centralized registry
   - Automatically loads sprite frames from `sprite_coords.json`
   - Defines satisfaction functions for placement rules
   - Provides `EntityFactory` for creating sprites by ID or name

### 2. **Updated `BoardTile` Base Class**
   - Added `load_from_def(definition: EntityDef)` method
   - Modified `satisfaction()` to use data-driven functions
   - Stores `_satisfaction_func` for custom placement rules

### 3. **Factory-Based Entity Creation**
   - `creatures.py`, `items.py`, `obstacles.py`, `spells.py` now export factory functions
   - Functions maintain backward compatibility with original API
   - All entities created through `entity_factory.create()` internally

### 4. **Centralized Configuration**
   - Sprite frames loaded from `sprite_coords.json`
   - Entity properties (xp, monster_level, etc.) defined as data
   - Placement rules defined as satisfaction functions

## Benefits

✅ **Single Sprite Source**: All sprite data now comes from `sprite_coords.json`
✅ **Easy Updates**: Change sprite frames in one place
✅ **Unified Treatment**: All entities are `BoardTile` sprites with consistent interface
✅ **Data-Driven**: Add new entities without creating new classes
✅ **Serializability**: Entities can be easily saved/loaded from JSON
✅ **Type Safety**: `EntityDef` dataclass provides structure
✅ **Flexible Satisfaction**: Custom placement rules as pluggable functions

## Usage Examples

### Creating Entities by ID
```python
from dragonsweepyr.monsters import entity_factory, TileID

# Create a specific creature
bat = entity_factory.create(TileID.Bat)
bat.tx, bat.ty = 5, 6  # Set position
board[5][6] = bat
```

### Creating Entities by Name
```python
# Alternative creation method
dragon = entity_factory.create_by_name("Dragon")
```

### Using Legacy Function API
```python
# Original imports still work (backward compatible)
from dragonsweepyr.monsters.creatures import Bat, Dragon
from dragonsweepyr.monsters.items import Orb, Treasure
from dragonsweepyr.monsters.obstacles import Wall, Decoration

bat = Bat(monster_level=3)
wall = Wall(contains=None)
treasure = Treasure(xp=5)
```

### Accessing the Global Factory
```python
from dragonsweepyr.monsters import entity_factory, ENTITY_REGISTRY

# Get all entities
all_entities = ENTITY_REGISTRY.values()

# Look up entity definition
dragon_def = entity_factory.get_definition(TileID.Dragon)
print(f"Dragon sprite frame: {dragon_def.sprite_frame}")
print(f"Dragon xp value: {dragon_def.xp}")
```

## Entity Registry Structure

The `ENTITY_REGISTRY` contains 34 entities organized by type:

### Creatures (21)
- Bat, BigSlime, DarkKnight, Death, Dragon, DragonEgg
- Eye, Fidel, Gargoyle, Gazer, Giant, Gnome, Guard
- Mimic, Mine, MineKing, Minotaur, Rat, RatKing, Skeleton, Slime, Snake, Wizard

### Items (5)
- Chest, Crown, Medikit, Orb, Treasure

### Obstacles (2)
- Wall, Decoration

### Spells (4)
- SpellDisarm, SpellMakeOrb, SpellRevealRats, SpellRevealSlimes

## Special Features

### Dynamic Sprite Frames
Some entities have dynamic sprite selection based on parameters:
- **DarkKnight**: Frame changes based on `monster_level` (5 vs 7)
- **Guard**: Frame changes based on `name` attribute (guard1-4)
- **Treasure**: Frame changes based on `xp` value (1, 3, or 5)
- **Mimic**: Can swap frames for mimicking state

### Placement Satisfaction Functions
Entities with special placement rules use satisfaction functions:
- **Dragon**: +10000 if in center region
- **MineKing**: +10000 if in corner
- **Wizard**: +10000 if on edge but not corner
- **Fidel**: +9000 if in corner
- **Guard**: +2500 if in assigned quadrant
- **Orb**: -10000 if near edge

## Backward Compatibility

All original factory function calls remain valid:
```python
# These still work exactly as before
from dragonsweepyr.monsters import creatures, items, obstacles, spells

bat = creatures.Bat(monster_level=2)
chest = items.Chest(contains=items.Treasure(5))
wall = obstacles.Wall()
spell = spells.SpellDisarm()
```

## Migration Path

If you encounter code using old class definitions:
1. Function names are unchanged - calls work as before
2. Functions now create sprites through `entity_factory.create()`
3. No code changes required for basic usage
4. For advanced usage, access `entity_factory` directly for more control

## File Structure

```
dragonsweepyr/monsters/
├── __init__.py                    # Exports entity_factory and ENTITY_REGISTRY
├── entity_definitions.py          # Data-driven entity system (NEW)
├── tiles.py                       # Updated BoardTile class
├── creatures.py                   # Factory functions (refactored)
├── items.py                       # Factory functions (refactored)
├── obstacles.py                   # Factory functions (refactored)
├── spells.py                      # Factory functions (refactored)
└── sprite_coords.json             # Sprite frame reference (unchanged)
```

## Performance Notes

- Sprite coordinates loaded once at module import
- Entity creation is lightweight (no class instantiation overhead)
- Registry lookup is O(1) hash table access
- Satisfaction functions are called only during placement evaluation

## Future Enhancements

The data-driven approach enables:
1. **JSON-based configuration**: Load entity data from JSON files
2. **Content editors**: Create new entities without code
3. **AI behaviors**: Store behavior trees as data
4. **Sound/animation mapping**: Associate sounds and animations with entities
5. **Serialization**: Save/load dungeon layouts with full entity data
6. **Modding support**: External entity packs
