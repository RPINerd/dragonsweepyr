import pygame

from dragonsweepyr.game import show_loading_c64

if __name__ == "__main__":
    pygame.init()
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)

    # Draw the sprites on a window for demonstration
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        show_loading_c64(screen)

        pygame.display.flip()

    pygame.quit()
