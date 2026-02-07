"""Main game application with a 13x10 grid."""
from __future__ import annotations

import logging
import random
import threading

import pygame

from dragonsweepyr.config import config
from dragonsweepyr.dungeon import Dungeon, generate_dungeon
from dragonsweepyr.logger import setup_logger
from dragonsweepyr.resources import assets

logger = setup_logger(__name__, level=logging.INFO)


class Game:

    """Manages the pygame window and grid rendering."""

    def __init__(self) -> None:
        """Initialize the game"""
        self.config = config

        self.window_width = self.config.grid_columns * self.config.tile_size
        self.window_height = self.config.grid_rows * self.config.tile_size + self.config.ui_height
        self.screen: pygame.Surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.config.window_title)

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running = False

        logger.info(
            f"Game window created: {self.window_width}x{self.window_height} "
            f"({self.config.grid_columns}x{self.config.grid_rows} grid)"
        )

        # Load assets into asset manager
        self.dungeon: Dungeon | None = None

    def _draw_grid(self) -> None:
        """Draw the grid on the screen."""
        if self.screen is None:
            return

        ts = self.config.tile_size

        # Draw vertical lines
        for x in range(self.config.grid_columns + 1):
            x_pos = x * ts
            pygame.draw.line(
                self.screen,
                self.config.grid_color,
                (x_pos, 0),
                (x_pos, self.config.grid_rows * ts),
            )

        # Draw horizontal lines
        for y in range(self.config.grid_rows + 1):
            y_pos = y * ts
            pygame.draw.line(
                self.screen,
                self.config.grid_color,
                (0, y_pos),
                (self.config.grid_columns * ts, y_pos),
            )

    def run(self) -> None:
        """Run the main game loop."""
        self.running = True

        # Load assets
        assets.load_all_sfx()

        # Track dungeon generation
        generation_error: Exception | None = None
        dungeon_ready = False

        def generate_dungeon_threaded() -> None:
            nonlocal generation_error, dungeon_ready
            try:
                self.dungeon = generate_dungeon()
                logger.info("Dungeon generated with sprites")
                dungeon_ready = True
            except Exception as e:
                generation_error = e
                logger.error(f"Failed to generate dungeon: {e}")

        # Start dungeon generation in background
        generation_thread = threading.Thread(target=generate_dungeon_threaded, daemon=True)
        generation_thread.start()

        # Show loading animation while dungeon generates
        minimum_load_duration = 0.5
        start_time = pygame.time.get_ticks()

        while True:
            elapsed_seconds = (pygame.time.get_ticks() - start_time) / 1000.0

            # Continue animation if: (1) minimum duration not met OR (2) dungeon not ready
            if elapsed_seconds < minimum_load_duration or not dungeon_ready:
                self.clock.tick(24)
                self.screen.fill("#4C596B")
                show_loading_c64(self.screen)
                pygame.display.flip()
            else:
                break

        # Check for errors during generation
        if generation_error is not None:
            raise generation_error

        try:
            while self.running:
                self._handle_events()
                self._update()
                self._render()

                assert self.clock is not None
                self.clock.tick(self.config.target_fps)
        finally:
            self.shutdown()

    def _handle_events(self) -> None:
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self) -> None:
        """Update game logic."""
        pass

    def _render(self) -> None:
        """Render the game window."""
        if self.screen is None:
            return

        self.screen.fill(self.config.background_color)
        self._draw_grid()
        if self.dungeon is not None:
            self.dungeon.dungeon_floor.tile_group.draw(self.screen)
        pygame.display.flip()

    @staticmethod
    def shutdown() -> None:
        """Clean up and close the game window."""
        pygame.quit()
        logger.info("Game closed")


def show_loading_c64(surface: pygame.Surface) -> None:
    """
    Display C64-style loading screen with random scanlines.

    Args:
        surface: Pygame surface to draw on.
    """
    colors = [
        "#000000", "#3e31a2", "#574200", "#8c3e34", "#545454",
        "#8d47b3", "#905f25", "#7abfc7", "#808080", "#68a941",
        "#bb776d", "#7abfc7", "#ababab", "#d0dc71", "#acea88",
        "#ffffff"
    ]
    band_height = 6

    band_count = int(config.window_height / band_height) + 1
    off_y = 0

    for _ in range(band_count):
        pygame.draw.rect(surface, random.choice(colors), (0, 0 + off_y, config.window_width, band_height))
        off_y += band_height


def main() -> None:
    """Main function to run the game."""
    pygame.init()
    logger.info("Pygame initialized")

    dragonsweepyr = Game()
    dragonsweepyr.run()
