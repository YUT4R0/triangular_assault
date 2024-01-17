import pygame
from screen_settings import WIDTH, MID_H, MID_W, REL_SIZE, screen
from styles import WHITE
pygame.init()

# horizontal walls
topper = pygame.Rect(0, MID_H - (REL_SIZE * 4), WIDTH, REL_SIZE)
bottom = pygame.Rect(0, MID_H + (REL_SIZE * 3), WIDTH, REL_SIZE)


def draw_lines():
    start_y = MID_H - (REL_SIZE * 4)
    end_y = MID_H + (REL_SIZE * 3)
    dot_size = 10
    dot_space = 5
    y = start_y
    while y < end_y:
        pygame.draw.line(screen, WHITE, (MID_W // 2, y), (MID_W // 2, y + dot_size))
        pygame.draw.line(screen, WHITE, (MID_W + MID_W // 2, y), (MID_W + MID_W // 2, y + dot_size))
        y += dot_size + dot_space
