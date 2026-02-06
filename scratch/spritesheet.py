import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import pygame

logger = logging.getLogger(__name__)

IMAGE_PATH = Path(__file__).parent.parent / "assets" / "sprites"


def _validate_positive_int(name: str, value: int) -> None:
    """
    Validate that a value is a positive integer.

    Args:
        name: Name of the parameter being validated.
        value: Value to validate.

    Raises:
        ValueError: If the value is not a positive integer.
    """
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value}.")


def _validate_non_negative_int(name: str, value: int) -> None:
    """
    Validate that a value is a non-negative integer.

    Args:
        name: Name of the parameter being validated.
        value: Value to validate.

    Raises:
        ValueError: If the value is negative.
    """
    if value < 0:
        raise ValueError(f"{name} must be a non-negative integer, got {value}.")


def grid_rects(
    sheet_size: tuple[int, int],
    sprite_width: int,
    sprite_height: int,
    *,
    margin: int = 0,
    spacing: int = 0,
) -> list[pygame.Rect]:
    """
    Build a list of rectangles for a grid-based spritesheet.

    Args:
        sheet_size: Width and height of the spritesheet.
        sprite_width: Width of each sprite.
        sprite_height: Height of each sprite.
        margin: Margin (in pixels) around the grid.
        spacing: Spacing (in pixels) between sprites.

    Returns:
        List of pygame.Rect objects for each sprite region.

    Raises:
        ValueError: If any dimension is invalid or no sprites fit.
    """
    _validate_positive_int("sprite_width", sprite_width)
    _validate_positive_int("sprite_height", sprite_height)
    _validate_non_negative_int("margin", margin)
    _validate_non_negative_int("spacing", spacing)

    sheet_width, sheet_height = sheet_size
    _validate_positive_int("sheet_width", sheet_width)
    _validate_positive_int("sheet_height", sheet_height)

    max_x = sheet_width - margin - sprite_width
    max_y = sheet_height - margin - sprite_height

    if max_x < margin or max_y < margin:
        raise ValueError("Sprites do not fit within the provided sheet size.")

    x_positions = range(margin, max_x + 1, sprite_width + spacing)
    y_positions = range(margin, max_y + 1, sprite_height + spacing)

    rects = [
        pygame.Rect(x, y, sprite_width, sprite_height)
        for y, x in product(y_positions, x_positions)
    ]

    if not rects:
        raise ValueError("No sprites could be generated from the given parameters.")

    return rects


@dataclass(frozen=True, slots=True)
class SpriteSheet:

    """
    Sprite sheet wrapper with slicing helpers.

    Attributes:
        image: Pygame surface containing the spritesheet image.
        width: Width of the spritesheet in pixels.
        height: Height of the spritesheet in pixels.
    """

    image: pygame.Surface
    width: int
    height: int

    @classmethod
    def from_file(cls, path: Path, *, convert_alpha: bool = True) -> "SpriteSheet":
        """
        Load a spritesheet from disk.

        Args:
            path: Path to the spritesheet image.
            convert_alpha: Whether to call convert_alpha for per-pixel alpha.

        Returns:
            SpriteSheet instance with the loaded image.
        """
        if not path.exists():
            raise FileNotFoundError(f"Spritesheet not found: {path}")

        image = pygame.image.load(path)
        image = image.convert_alpha() if convert_alpha else image.convert()
        width, height = image.get_size()

        logger.debug("Loaded spritesheet %s (%dx%d)", path, width, height)
        return cls(image=image, width=width, height=height)

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> "SpriteSheet":
        """
        Create a spritesheet from an existing surface.

        Args:
            surface: Surface to wrap.

        Returns:
            SpriteSheet instance for the provided surface.
        """
        width, height = surface.get_size()
        return cls(image=surface, width=width, height=height)

    def slice_grid(
        self,
        sprite_width: int,
        sprite_height: int,
        *,
        margin: int = 0,
        spacing: int = 0,
        max_sprites: int | None = None,
    ) -> list[pygame.Surface]:
        """
        Slice the spritesheet into a grid of sprites.

        Args:
            sprite_width: Width of each sprite.
            sprite_height: Height of each sprite.
            margin: Margin (in pixels) around the grid.
            spacing: Spacing (in pixels) between sprites.
            max_sprites: Optional limit on number of sprites to return.

        Returns:
            List of sprite surfaces.
        """
        rects = grid_rects(
            (self.width, self.height),
            sprite_width,
            sprite_height,
            margin=margin,
            spacing=spacing,
        )
        return self.slice_rects(rects, max_sprites=max_sprites)

    def slice_rects(
        self,
        rects: Sequence[pygame.Rect],
        *,
        max_sprites: int | None = None,
    ) -> list[pygame.Surface]:
        """
        Slice the spritesheet using explicit rectangles.

        Args:
            rects: Rectangles to extract from the spritesheet.
            max_sprites: Optional limit on number of sprites to return.

        Returns:
            List of sprite surfaces.
        """
        sprites: list[pygame.Surface] = []

        for rect in rects:
            sprite = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            sprite.blit(self.image, (0, 0), rect)
            sprites.append(sprite)

            if max_sprites is not None and len(sprites) >= max_sprites:
                break

        logger.debug("Sliced %d sprites from spritesheet", len(sprites))
        return sprites


def slice_surface(
    surface: pygame.Surface,
    sprite_width: int,
    sprite_height: int,
    *,
    margin: int = 0,
    spacing: int = 0,
    max_sprites: int | None = None,
) -> list[pygame.Surface]:
    """
    Slice an arbitrary surface into sprites.

    Args:
        surface: Surface to slice.
        sprite_width: Width of each sprite.
        sprite_height: Height of each sprite.
        margin: Margin (in pixels) around the grid.
        spacing: Spacing (in pixels) between sprites.
        max_sprites: Optional limit on number of sprites to return.

    Returns:
        List of sprite surfaces.
    """
    sheet = SpriteSheet.from_surface(surface)
    return sheet.slice_grid(
        sprite_width,
        sprite_height,
        margin=margin,
        spacing=spacing,
        max_sprites=max_sprites,
    )


def load_and_slice(
    path: Path,
    sprite_width: int,
    sprite_height: int,
    *,
    margin: int = 0,
    spacing: int = 0,
    max_sprites: int | None = None,
    convert_alpha: bool = True,
) -> list[pygame.Surface]:
    """
    Load a spritesheet from disk and slice it into sprites.

    Args:
        path: Path to the spritesheet image.
        sprite_width: Width of each sprite.
        sprite_height: Height of each sprite.
        margin: Margin (in pixels) around the grid.
        spacing: Spacing (in pixels) between sprites.
        max_sprites: Optional limit on number of sprites to return.
        convert_alpha: Whether to call convert_alpha for per-pixel alpha.

    Returns:
        List of sprite surfaces.
    """
    sheet = SpriteSheet.from_file(path, convert_alpha=convert_alpha)
    return sheet.slice_grid(
        sprite_width,
        sprite_height,
        margin=margin,
        spacing=spacing,
        max_sprites=max_sprites,
    )


def iter_grid_positions(
    sheet_size: tuple[int, int],
    sprite_width: int,
    sprite_height: int,
    *,
    margin: int = 0,
    spacing: int = 0,
) -> Iterable[tuple[int, int]]:
    """
    Yield grid positions for a spritesheet.

    Args:
        sheet_size: Width and height of the spritesheet.
        sprite_width: Width of each sprite.
        sprite_height: Height of each sprite.
        margin: Margin (in pixels) around the grid.
        spacing: Spacing (in pixels) between sprites.

    Yields:
        Tuples of (x, y) positions for each sprite origin.
    """
    rects = grid_rects(
        sheet_size,
        sprite_width,
        sprite_height,
        margin=margin,
        spacing=spacing,
    )
    for rect in rects:
        yield rect.x, rect.y


def load_spritesheet(
    filename: str, sprite_width: int, sprite_height: int
) -> list[pygame.Surface]:
    """
    Load a spritesheet and split it into individual sprites.

    Args:
        filename: Path to the spritesheet image file.
        sprite_width: Width of each individual sprite.
        sprite_height: Height of each individual sprite.

    Returns:
        List of individual sprite surfaces.
    """
    sprites: list[pygame.Surface] = []
    sheet_path = IMAGE_PATH / filename
    spritesheet = pygame.image.load(sheet_path).convert_alpha()
    sheet_width, sheet_height = spritesheet.get_size()

    for y in range(0, sheet_height, sprite_height):
        for x in range(0, sheet_width, sprite_width):
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(spritesheet, (0, 0), (x, y, sprite_width, sprite_height))
            sprites.append(sprite)

    print(f"Spritesheet '{filename}' loaded with {len(sprites)} sprites.")

    return sprites


if __name__ == "__main__":
    pygame.init()
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)

    # sprites = load_spritesheet("buttons30x30.png", 30, 30)
    sprites = load_and_slice(
        IMAGE_PATH / "monsters.png", 16, 16)
    print(f"Total sprites loaded: {len(sprites)}")

    # Draw the sprites on a window for demonstration
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i, sprite in enumerate(sprites):
            x = (i % 10) * 16
            y = (i // 10) * 16
            screen.blit(sprite, (x, y))

        scaled_screen = pygame.transform.scale2x(screen)
        screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()

    pygame.quit()
