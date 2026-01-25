# Happiness Function Breakdown

## Overview

The `happiness()` function is a scoring algorithm used during dungeon generation to influence desired placement of actors (monsters, items, and objects) on the game board.

The function returns a numeric score where higher values indicate better/more desirable configurations.

Called repeatedly during the board generation process to iteratively improve actor positions by swapping them around until an optimal (highest happiness) configuration is achieved.

## Scoring System

### DragonEgg

- **Condition**: Close to a Dragon (distance < 1.5)
- **Score**: +9,000
- **Purpose**: Ensures dragon eggs spawn near dragons

### Fidel

- **Condition**: Positioned in a corner
- **Score**: +9,000
- **Purpose**: Prefers Fidel to be in corner positions
- **Note**: There's commented-out code that would penalize Fidel being close to chests

### Gnome

- **Condition**: Close to a Medikit (distance < 1.5)
- **Score**: +10,000
- **Purpose**: Ensures gnomes spawn near health items
- **Note**: There's commented-out code for an alternate gnome placement strategy using "favorite jump targets"

### Rat (Guard Variant)

- **Condition**: Named "rat_guard", horizontally adjacent to Rat King (distance = 1, same Y coordinate)
- **Score**: +1,000
- **Purpose**: Positions guard rats next to the Rat King in a horizontal line

### Guard

- **Condition**: Positioned in correct quadrant based on guard name
- **Score**: +2,500
- **Purpose**: Each of the 4 guards should be in their designated quadrant
- **Logic**: Handled by `isGuardianInRightQuadrant()` function

### Giant

- **Conditions**:
  1. Romeo on left side (tx ≤ 5) or Juliet on right side (tx ≥ 7): +1,000
  2. Both giants on same row with equal distance from center: +10,000
- **Total Possible Score**: +11,000
- **Purpose**: Creates "Romeo and Juliet" scenario - giants on opposite sides, same row, symmetrically positioned around center

### BigSlime

- **Condition**: Close to a Wizard (distance < 1.5)
- **Score**: +1,000
- **Purpose**: Pairs big slimes with wizards

### Wizard

- **Condition**: On an edge but not in a corner
- **Score**: +10,000
- **Purpose**: Positions wizards on board edges while avoiding corners

### MineKing

- **Condition**: Positioned in a corner
- **Score**: +10,000
- **Purpose**: Ensures Mine King spawns in a corner

### Dragon

- **Condition**: At horizontal center, Y=4 (center position: [6, 4] for 13-wide grid)
- **Score**: +10,000
- **Purpose**: Places dragon at the center of the board

### Minotaur

- **Conditions**:
  - Must be near exactly 1 chest (distance < 2)
  - No other minotaurs near that same chest
- **Score**: +10,000 (if conditions met)
- **Purpose**: Each minotaur guards exactly one chest, without crowding

### Gargoyle

- **Condition**: In correct position relative to twin gargoyle
- **Score**: +1,000
- **Purpose**: Positions paired gargoyles correctly
- **Logic**: Handled by `isGargoyleInRightPlace()` function

### Orb

**Multiple scoring rules:**

1. **Position Penalty**
   - **Condition**: Close to board edge
   - **Score**: -10,000
   - **Purpose**: Keeps orbs away from edges

2. **Forbidden Object Penalty**
   - **Condition**: Reveals forbidden objects within orb radius
   - **Forbidden Objects**: Dragon, Gazer, Chest, SpellMakeOrb, RatKing, Mine, Fidel, DragonEgg, BigSlime, Mimic
   - **Score**: -2,000 per forbidden object
   - **Purpose**: Prevents orbs from revealing critical objects

3. **Wall Penalty**
   - **Condition**: Reveals more than 2 walls
   - **Score**: -2,000 per wall beyond 2
   - **Purpose**: Limits wall visibility

4. **Medikit/Wall Bonus**
   - **Condition**: Reveals exactly 1 medikit AND at least 1 wall
   - **Score**: +2,000
   - **Purpose**: Encourages useful orb placements that reveal health and walls

**Total Possible Range**: -10,000 (edge placement) + additional penalties/bonuses based on revealed objects

### Medikit

- **Condition**: Counts nearby medikits (distance < 3.5)
- **Score**: -1,000 per nearby medikit
- **Purpose**: Spreads medikits out across the board

### Chest

- **Condition**: Counts nearby chests (distance < 3)
- **Score**: -1,000 per nearby chest
- **Purpose**: Spreads chests out across the board

### Wall

**Complex scoring based on wall clustering:**

1. Count adjacent walls (distance ≤ 1)
2. Count diagonal walls (distance < 1.5)
3. Count if wall is on edge

**Bonus Condition**:

- Exactly 1 adjacent wall
- No diagonal walls
- Less than 2 walls (including self) on edges

**Score**: +2,000
**Purpose**: Encourages pairs of walls in non-edge positions, creating strategic obstacles

## Helper Function

### countNearMeWithSameId(a, minDistance)

- Counts how many actors of the same type are within a specified distance
- Used by Medikit, Chest, and Wall scoring
- Purpose: Implements spacing/clustering logic

## Score Ranges

| Actor Type | Min Score | Max Score | Notes |
| ---------- | --------- | --------- | ----- |
| DragonEgg | 0 | 9,000 | Binary: near dragon or not |
| Fidel | 0 | 9,000 | Binary: in corner or not |
| Gnome | 0 | 10,000 | Binary: near medikit or not |
| Rat (guard) | 0 | 1,000 | Binary: guarding king or not |
| Guard | 0 | 2,500 | Binary: in quadrant or not |
| Giant | 0 | 11,000 | 1,000 + 10,000 for full setup |
| BigSlime | 0 | 1,000 | Binary: near wizard or not |
| Wizard | 0 | 10,000 | Binary: edge-but-not-corner or not |
| MineKing | 0 | 10,000 | Binary: in corner or not |
| Dragon | 0 | 10,000 | Binary: at center or not |
| Minotaur | 0 | 10,000 | Binary: guarding one chest or not |
| Gargoyle | 0 | 1,000 | Binary: correct twin position or not |
| Orb | -∞ | 2,000 | Complex penalty/bonus system |
| Medikit | -∞ | 0 | Penalty for clustering |
| Chest | -∞ | 0 | Penalty for clustering |
| Wall | 0 | 2,000 | Bonus for specific configurations |

## Constants Referenced

- `ORB_RADIUS`: The radius within which an orb reveals other objects (not shown in this excerpt)
- Grid dimensions: `state.gridW` and `state.gridH` (13x10 based on context)
