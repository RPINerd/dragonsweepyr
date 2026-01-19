# Board Generation Overview

## Lifecycle entry points

- A new run calls `newGame()` which resets `GameState`, restores player HP to 6, flags the status as `generating`, and delays generation by one frame so the render loop can show the loading screen ([archive/game.js](archive/game.js#L437-L456)).
- The main loop steps through `updateGeneratingDungeon()`: it burns the initial frame, invokes `generateDungeon()`, then waits one more frame before switching `state.status` to `playing` and starting the timer ([archive/game.js](archive/game.js#L2072-L2121)).

## Grid bootstrap

- The board is always 13x10 tiles; placeholders for every coordinate are pre-created as `Empty` actors with attached "button" frame IDs drawn from a shuffled bag (corners get fixed frames, dragon tile later clears its button) ([archive/game.js](archive/game.js#L458-L520)).

## Layered placement algorithm

- Generation uses layers. Each `beginLayer()`/`add()`/`endLayer()` trio queues prototypes, places them into available empty tiles, then improves placements with a "happiness" score search ([archive/game.js](archive/game.js#L522-L740)).
- Placement search: for up to four passes it shuffles all tiles, tries swapping each newly placed actor with any non-fixed actor, and keeps the swap if happiness is not worse. When a layer is finalized, its actors become `fixed`, so later layers cannot displace them.

## What each layer adds (in order)

- Layer 1: 1 Dragon (level 13, revealed later), 1 Wizard (level 1) ([archive/game.js](archive/game.js#L492-L501), [archive/game.js](archive/game.js#L1657-L1670)).
- Layer 2: 5 Big Slimes (level 8) ([archive/game.js](archive/game.js#L503-L508), [archive/game.js](archive/game.js#L1671-L1683)).
- Layer 3: 1 Mine King (level 10) ([archive/game.js](archive/game.js#L510-L515), [archive/game.js](archive/game.js#L1607-L1621)).
- Layer 4: 2 Giants (level 9) named romeo and juliet to enable their pairing rules ([archive/game.js](archive/game.js#L517-L523), [archive/game.js](archive/game.js#L1698-L1711)).
- Layer 5 (bosses, elites, utility, loot): Rat King; 6 Walls each containing Treasure (xp1); 5 Minotaurs; 4 Guards named guard1–4; 8 Gargoyles (2 per name gargoyle1–4); 2 Gazers; 9 Mines; 5 Medikits; 3 Chests with Treasure (xp5); 2 Chests with Medikits; 1 always-revealed Orb named `orb_with_healing`; 1 Dragon Egg ([archive/game.js](archive/game.js#L525-L556)).
- Layer 6 (fodder and specials): 13 Rats (lvl1), 12 Bats (lvl2), 10 Skeletons (lvl3), 8 Slimes (lvl5), 1 Mimic (lvl11), 1 Gnome (xp9, lvl0), 1 SpellMakeOrb scroll ([archive/game.js](archive/game.js#L558-L571)).

## Happiness scoring (placement heuristics)

- Dragon Egg close to Dragon (<1.5) +9000; Dragon centered at (6,4) +10000 ([archive/game.js](archive/game.js#L592-L652)).
- Giants: romeo prefers left half, juliet right; huge bonus when both share a row and are symmetric around center ([archive/game.js](archive/game.js#L608-L622)).
- Mine King prefers corners; Wizard prefers edges but not corners; Big Slime near Wizard; Gnome near Medikit ([archive/game.js](archive/game.js#L599-L656)).
- Guards score when inside their name-specific quadrant; Gargoyles score when a named twin is adjacent (and later get orientation set) ([archive/game.js](archive/game.js#L569-L596)).
- Minotaur prefers being within <2 of exactly one chest without overlapping another Minotaur’s chest ([archive/game.js](archive/game.js#L623-L646)).
- Orb penalized near edges and near forbidden objects (Dragon, Gazer, Chest, SpellMakeOrb, Rat King, Mine, Fidel, Dragon Egg, Big Slime, Mimic); bonuses/penalties based on what it would reveal within radius 2.1 ([archive/game.js](archive/game.js#L650-L688)).
- Medikit and Chest are anti-clustered; Walls rewarded when forming small single-adjacent pairs away from edges ([archive/game.js](archive/game.js#L690-L734)).

## Post-processing after placement

- Guards get sprite variants by name; Minotaurs remember the coordinates of a nearby chest; Dragon is auto-revealed and its UI button is cleared ([archive/game.js](archive/game.js#L740-L773)).
- Gargoyles orient their sprites to face their named twin; Walls receive cyclical HP from the `[3,3,3,3,3,3]` list and positions are logged; chest positions are recorded too ([archive/game.js](archive/game.js#L774-L808)).
- `computeStats()` tallies totals, XP (including chest contents), and projected player HP curve up to max level; debug-only `checkLevel()` validates key placements in non-release builds ([archive/game.js](archive/game.js#L810-L910)).

## Start of play

- After one frame of post-generation pause, the game switches to `playing`, enabling input and starting the run timer ([archive/game.js](archive/game.js#L2072-L2121)).
