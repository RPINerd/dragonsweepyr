"""Module for handing asset loading and rendering."""

import logging

import pygame

from dragonsweepyr.const import IMAGE_PATH, MUSIC_PATH, SFX_PATH

logger = logging.getLogger(__name__)


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
