from pathlib import Path

import pygame

IMAGE_PATH = Path(__file__).parent.parent / "assets" / "images"


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
    window_size = (600, 300)
    screen = pygame.display.set_mode(window_size)

    sprites = load_spritesheet("buttons30x30.png", 30, 30)
    print(f"Total sprites loaded: {len(sprites)}")

    # Draw the sprites on a window for demonstration
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i, sprite in enumerate(sprites):
            x = (i % 10) * 30
            y = (i // 10) * 30
            screen.blit(sprite, (x, y))

        pygame.display.flip()

    pygame.quit()
