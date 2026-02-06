"""Module for handing asset loading and rendering."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame

from dragonsweepyr.const import IMAGE_PATH, MUSIC_PATH, SFX_PATH, SPRITE_PATH

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class SpriteSheet:

    """Class to handle loading and slicing spritesheets."""

    def __init__(self, filename: str, sprite_width: int, sprite_height: int) -> None:
        """Initialize and load the spritesheet."""
        self.sprite_file: Path = SPRITE_PATH / filename
        self.sprite_width: int = sprite_width
        self.sprite_height: int = sprite_height
        self.sprites: list[list[pygame.Surface]] = []
        self._load_and_slice()

    def _load_and_slice(self) -> None:
        """Load the spritesheet and slice it into individual sprites."""
        spritesheet = pygame.image.load(self.sprite_file).convert_alpha()
        sheet_width, sheet_height = spritesheet.get_size()

        for y in range(0, sheet_height, self.sprite_height):
            row: list[pygame.Surface] = []
            for x in range(0, sheet_width, self.sprite_width):
                sprite = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
                sprite.blit(spritesheet, (0, 0), (x, y, self.sprite_width, self.sprite_height))
                row.append(sprite)
            self.sprites.append(row)
        logger.debug(f"Spritesheet '{self.sprite_file}' loaded with {len(self.sprites)} rows of sprites.")

    def get_sprite(self, row: int, col: int) -> pygame.Surface:
        """Get a specific sprite from the spritesheet."""
        try:
            return self.sprites[row][col]
        except IndexError:
            logger.error(f"Requested sprite from {self.sprite_file.name} at row {row}, col {col} is out of bounds.")
            return pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)


class AssetManager:

    """Singleton asset manager for centralized access to game assets."""

    _instance: AssetManager | None = None

    def __init__(self) -> None:
        """Initialize asset manager attributes."""
        self.blank_sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        self._monster_spritesheet: SpriteSheet | None = None
        self.sfx: dict[str, pygame.mixer.Sound] = {}

    def __new__(cls) -> AssetManager:
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def monster_spritesheet(self) -> SpriteSheet:
        """Lazy load the monster spritesheet on first access."""
        if self._monster_spritesheet is None:
            self._monster_spritesheet = SpriteSheet("monsters.png", 16, 16)
        return self._monster_spritesheet

    def load_all_sfx(self) -> None:
        """Load all sound effects."""
        self.sfx = load_sfx()


# Global asset manager instance
assets = AssetManager()


def load_music() -> None:
    """Load music files into memory."""
    for music_file in MUSIC_PATH.glob("*.mp3"):
        pygame.mixer.music.load(music_file)

    logger.info("Music files loaded...")
    logger.debug(f"Loaded music files: {pygame.mixer.music.get_busy()}")


def load_sfx() -> dict[str, pygame.mixer.Sound]:
    """Load sound effect files into memory."""
    sfx_dict: dict[str, pygame.mixer.Sound] = {}

    for sfx_file in SFX_PATH.glob("*.wav"):
        sound_name = sfx_file.stem
        sfx_dict[sound_name] = pygame.mixer.Sound(sfx_file)

    logger.info("Sound effect files loaded...")
    logger.debug(f"Loaded SFX files: {list(sfx_dict.keys())}")

    return sfx_dict


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

    logger.info(f"Spritesheet '{filename}' loaded with {len(sprites)} sprites.")

    return sprites
