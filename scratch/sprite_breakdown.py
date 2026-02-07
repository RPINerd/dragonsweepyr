"""Extract sprites from a spritesheet using coordinate metadata."""

from __future__ import annotations

import argparse
import json
import logging
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pygame

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class SpriteCoord:

    """
    Coordinates and size for a sprite in the sheet.

    Attributes:
        x: Top-left x coordinate in the sheet.
        y: Top-left y coordinate in the sheet.
        width: Sprite width.
        height: Sprite height.
        pivot_x: Horizontal pivot offset for rendering (not used for cropping).
        pivot_y: Vertical pivot offset for rendering (not used for cropping).
    """

    x: int
    y: int
    width: int
    height: int
    pivot_x: int
    pivot_y: int


def parse_sprite_coords(data: Mapping[str, Any]) -> dict[str, SpriteCoord]:
    """
    Parse sprite coordinates from JSON content.

    Args:
        data: Raw JSON mapping of sprite names to coordinate data.

    Returns:
        Parsed sprite coordinates keyed by sprite name.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    coords: dict[str, SpriteCoord] = {}
    for name, payload in data.items():
        if not isinstance(payload, Mapping):
            raise ValueError(f"Sprite '{name}' value must be an object.")
        required = ("x", "y", "width", "height")
        missing = [key for key in required if key not in payload]
        if missing:
            raise ValueError(f"Sprite '{name}' missing keys: {', '.join(missing)}")
        try:
            x = int(payload["x"])
            y = int(payload["y"])
            width = int(payload["width"])
            height = int(payload["height"])
            pivot_x = int(payload.get("pivot_x", 0))
            pivot_y = int(payload.get("pivot_y", 0))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Sprite '{name}' has non-integer values.") from exc
        if width <= 0 or height <= 0:
            raise ValueError(f"Sprite '{name}' has invalid size {width}x{height}.")
        coords[name] = SpriteCoord(
            x=x,
            y=y,
            width=width,
            height=height,
            pivot_x=pivot_x,
            pivot_y=pivot_y,
        )
    return coords


def load_coords(coords_path: Path) -> dict[str, SpriteCoord]:
    """
    Load sprite coordinates from a JSON file.

    Args:
        coords_path: Path to the JSON coordinate file.

    Returns:
        Parsed sprite coordinates keyed by sprite name.
    """
    with coords_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, Mapping):
        raise ValueError("Coordinates JSON must be an object at the top level.")
    return parse_sprite_coords(data)


def extract_sprite(sheet: pygame.Surface, coord: SpriteCoord) -> pygame.Surface:
    """
    Extract a single sprite surface from the sheet.

    Args:
        sheet: Loaded spritesheet surface.
        coord: Coordinates describing the sprite bounds.

    Returns:
        A surface containing the sprite pixels.
    """
    rect = pygame.Rect(coord.x, coord.y, coord.width, coord.height)
    sprite = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), rect)
    return sprite


def extract_all_sprites(
    sheet_path: Path,
    coords_path: Path,
    output_dir: Path,
) -> list[Path]:
    """
    Extract all sprites and write them as PNG files.

    Args:
        sheet_path: Path to the spritesheet image.
        coords_path: Path to the JSON coordinate file.
        output_dir: Directory to write PNG files to.

    Returns:
        List of output file paths written.
    """
    if "SDL_VIDEODRIVER" not in os.environ:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    try:
        sheet = pygame.image.load(sheet_path)
        coords = load_coords(coords_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        written: list[Path] = []
        sheet_rect = sheet.get_rect()
        for name, coord in coords.items():
            rect = pygame.Rect(coord.x, coord.y, coord.width, coord.height)
            if not sheet_rect.contains(rect):
                LOGGER.warning("Skipping %s; rect %s outside sheet bounds %s", name, rect, sheet_rect)
                continue
            sprite = extract_sprite(sheet, coord)
            output_path = output_dir / f"{name}.png"
            pygame.image.save(sprite, output_path)
            written.append(output_path)
        return written
    finally:
        pygame.quit()


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build the CLI argument parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Extract sprites from a spritesheet.")
    parser.add_argument(
        "--sheet",
        type=Path,
        required=True,
        help="Path to the spritesheet image.",
    )
    parser.add_argument(
        "--coords",
        type=Path,
        required=True,
        help="Path to the JSON coordinate file.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Directory to write extracted PNG files.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser


def main() -> int:
    """
    Run the sprite extraction script.

    Returns:
        Process exit code.
    """
    parser = build_arg_parser()
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))
    try:
        written = extract_all_sprites(args.sheet, args.coords, args.out_dir)
    except (OSError, ValueError, pygame.error) as exc:
        LOGGER.error("Extraction failed: %s", exc)
        return 1

    LOGGER.info("Wrote %d sprites to %s", len(written), args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
