# Using add_tile() Method

The `add_tile()` method provides a clean way to add tiles to the dungeon floor with custom properties.

## Basic Usage

```python
# Add a single tile
floor.add_tile(creatures.Dragon)

# Add multiple tiles
floor.add_tile(creatures.Rat, count=13)
```

## With Parameters

```python
# Add tiles with monster level
floor.add_tile(creatures.BigSlime, count=5, monster_level=8)

# Add tiles with contained items
floor.add_tile(obstacles.Wall, count=6, contains=items.Treasure(1))

# Add tiles with custom names
guards = floor.add_tile(creatures.Guard, count=1, monster_level=7, name="guard1")
```

## All Supported Parameters

The method accepts any valid `BoardTile` attribute via `**kwargs`:

- `monster_level`: Monster's level
- `name`: Custom identifier
- `contains`: Item contained in the tile
- `revealed`: Whether the tile is initially revealed
- `fixed`: Whether the tile position is fixed
- `wallHP` / `wallMaxHP`: For wall tiles
- Any other `BoardTile` attribute
