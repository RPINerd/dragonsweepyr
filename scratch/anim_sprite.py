
import sys

import pygame

spritesheet = sys.argv[1]
rows = int(sys.argv[2])
cols = int(sys.argv[3])
total_frames = int(sys.argv[4])

pygame.init()
pygame.display.set_caption("Animation Test")

# Load sheet first to get dimensions
sheet = pygame.image.load(spritesheet)
sheet_rect = sheet.get_rect()
frame_width = sheet_rect.width // cols
frame_height = sheet_rect.height // rows

# Set up display before converting
screen = pygame.display.set_mode((frame_width, frame_height))
sheet = sheet.convert_alpha()
clock = pygame.time.Clock()
frames = []
for i in range(total_frames):
    row = i // cols
    col = i % cols
    rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
    frame = sheet.subsurface(rect)
    frames.append(frame)

frame_index = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(frames[frame_index], (0, 0))
    pygame.display.flip()
    frame_index = (frame_index + 1) % total_frames
    clock.tick(60)

pygame.quit()
