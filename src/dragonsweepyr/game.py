"""Main game application with a 13x10 grid."""
from __future__ import annotations

import pygame

from dragonsweepyr.config import GameConfig
from dragonsweepyr.logger import LOGGER, setup_logger


class GameWindow:

    """Manages the pygame window and grid rendering."""

    def __init__(self, config: GameConfig) -> None:
        """
        Initialize the game window.

        Args:
            config: GameConfig instance. Defaults to GameConfig() if None.
        """
        self.config = config
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.running = False

    def initialize(self) -> None:
        """Initialize pygame and create the game window."""
        pygame.init()
        LOGGER.info("Pygame initialized")

        window_width = self.config.grid_columns * self.config.tile_size
        window_height = self.config.grid_rows * self.config.tile_size + self.config.ui_height

        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(self.config.window_title)
        self.clock = pygame.time.Clock()

        LOGGER.info(
            f"Game window created: {window_width}x{window_height} "
            f"({self.config.grid_columns}x{self.config.grid_rows} grid)"
        )

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
        self.initialize()
        self.running = True

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
        pygame.display.flip()

    def shutdown(self) -> None:
        """Clean up and close the game window."""
        pygame.quit()
        LOGGER.info("Game closed")


def main() -> None:
    """Main function to run the game."""
    setup_logger()
    config = GameConfig()
    game_window = GameWindow(config)
    game_window.run()


if __name__ == "__main__":
    main()
