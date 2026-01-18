# Code Structure Ramblings

## Player

Type: Class

```python
max_hp = 4
current_hp = self.max_hp
xp = 0
level = 1
score = 0
```

## Game

### States

Type: Custom class

Playing - game board, with tiles/health etc

Dead

Win

Loading - during field generation

### Global Stats

Type: class

```python
total = 0
empties = 0
totalXP = 0
xpRequiredToMax = 0
excessXP = 0
totalHPOnMaxLevel = 0
totalMonsterHP = 0
```

### New Game

New `GameState`
player level = 1
player max_hp = 6
player_hp = max_hp

generateDungeon
    wait

crown animation loop start?


## Tiles

### TileID

Probably an enum?

```ini
None = "none"
Empty = "empty"
Orb = "orb"
SpellMakeOrb = "spell_reveal"
Mine = "mine"
MineKing = "mine king"
Dragon = "dragon"
Wall = "wall"
Mimic = "mimic"
Medikit = "medikit"
RatKing = "rat king"
Rat = "rat"
Slime = "slime"
Gargoyle = "gargoyle"
Minotaur = "minotaur"
Chest = "chest"
Skeleton = "skeleton"
Treasure = "treasure"
Snake = "snake"
Giant = "giant"
Decoration = "decoration"
Wizard = "wizard"
Gazer = "gazer"
SpellDisarm = "spell_disarm"
BigSlime = "big slime"
SpellRevealRats = "spell_reveal_rats"
SpellRevealSlimes = "spell_reveal_slimes"
Gnome = "gnome"
Bat = "bat"
Guard = "guardian"
Crown = "crown"
Fidel = "fidel"
DragonEgg = "dragon_egg"
```

### Individual Tile

Type: class

```python
tx = 0
ty = 0
fixed = false
id = TileID.None
strip = null
stripFrame = 0
deadStripFrame = 0
revealed = false
monsterLevel = 0
xp = 0
mimicMimicking = false; // TODO: necessary
defeated = false
mark = 0
trapDisarmed = false
contains = null
wallHP = 0
wallMaxHP = 0
isMonster = false
name = "none"
minotaurChestLocation = [-1, -1]
```

## Perpetual config

Aka nomicon

### Load

nomicon read? - yes/no
sound - on/off
music - on/off
collected stamps - STAMP_SPEC_IDS

### Save

set read/sound/music
for stamp in collected, set to collected
