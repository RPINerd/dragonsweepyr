"""Script to test out dungeon generation."""

from time import perf_counter

from dragonsweepyr.dungeon import Dungeon, Floor, generate_dungeon

if __name__ == "__main__":
    print("Generating test dungeon...")
    start_time = perf_counter()
    test_dungeon: Dungeon = generate_dungeon()
    end_time = perf_counter()
    print(f"Dungeon generation complete in {end_time - start_time:.4f} seconds.")

    test_floor: Floor = test_dungeon.dungeon_floor
    print("Generated Floor Layout:")
    test_floor.render_floor()
