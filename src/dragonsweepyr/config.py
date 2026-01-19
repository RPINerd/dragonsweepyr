"""Game configuration and settings."""

from dataclasses import dataclass


@dataclass
class GameConfig:

    """Configuration for game behavior and appearance."""

    # Display settings
    window_title: str = "Dragon Sweepyr"
    window_width: int = 800
    window_height: int = 800
    ui_height: int = 100
    target_fps: int = 30
    # fullscreen: bool = False
    background_color: tuple[int, int, int] = (16, 16, 20)

    # Grid settings
    grid_columns: int = 13
    grid_rows: int = 10
    tile_size: int = 48  # ? maybe drop
    grid_offset_x: int = 50
    grid_offset_y: int = 50
    show_grid: bool = True
    grid_color: tuple[int, int, int] = (100, 100, 100)

    # Audio settings
    master_volume: float = 1.0
    sound_volume: float = 1.0
    music_volume: float = 0.7

    # Game settings
    starting_hp: int = 6
    enable_hints: bool = True
    animation_speed: float = 1.0

    # Debug settings
    debug_mode: bool = True
    show_all_tiles: bool = False
    god_mode: bool = False


# Global config instance
config = GameConfig()


def load_config() -> GameConfig:
    """
    Load configuration from file or return defaults.

    Returns:
        Game configuration
    """
    # For now, just return default config
    # Could be extended to load from a config file
    return config


def save_config(cfg: GameConfig) -> None:
    """
    Save configuration to file.

    Args:
        cfg: Configuration to save
    """
    # Could be extended to save to a config file
    pass
