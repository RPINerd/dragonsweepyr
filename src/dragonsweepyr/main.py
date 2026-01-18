"""Main game application with a 13x10 grid."""
from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from dragonsweepyr.logger import LOGGER, setup_logger


@dataclass
class GameConfig:

    """Configuration for the game window and grid."""

    grid_width: int = 13
    grid_height: int = 10
    tile_size: int = 48
    fps: int = 60
    window_title: str = "Dragonsweep"
    background_color: tuple[int, int, int] = field(default_factory=lambda: (16, 16, 20))
    grid_color: tuple[int, int, int] = field(default_factory=lambda: (100, 100, 100))


class GameWindow:

    """Manages the pygame window and grid rendering."""

    def __init__(self, config: GameConfig | None = None) -> None:
        """
        Initialize the game window.

        Args:
            config: GameConfig instance. Defaults to GameConfig() if None.
        """
        self.config = config or GameConfig()
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.running = False

    def initialize(self) -> None:
        """Initialize pygame and create the game window."""
        pygame.init()
        LOGGER.info("Pygame initialized")

        window_width = self.config.grid_width * self.config.tile_size
        window_height = self.config.grid_height * self.config.tile_size

        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(self.config.window_title)
        self.clock = pygame.time.Clock()

        LOGGER.info(
            f"Game window created: {window_width}x{window_height} "
            f"({self.config.grid_width}x{self.config.grid_height} grid)"
        )

    def _draw_grid(self) -> None:
        """Draw the grid on the screen."""
        if self.screen is None:
            return

        ts = self.config.tile_size

        # Draw vertical lines
        for x in range(self.config.grid_width + 1):
            x_pos = x * ts
            pygame.draw.line(
                self.screen,
                self.config.grid_color,
                (x_pos, 0),
                (x_pos, self.config.grid_height * ts),
            )

        # Draw horizontal lines
        for y in range(self.config.grid_height + 1):
            y_pos = y * ts
            pygame.draw.line(
                self.screen,
                self.config.grid_color,
                (0, y_pos),
                (self.config.grid_width * ts, y_pos),
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
                self.clock.tick(self.config.fps)
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
