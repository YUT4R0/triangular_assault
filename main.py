import pygame
import random
import sys

pygame.init()
pygame.font.init()


def update_screen():
    pygame.display.flip()
    pygame.time.Clock().tick(60)


def draw_screen():
    screen.fill(black)
    pygame.draw.polygon(screen, white, player_r)


# colors
white = (255, 255, 255)
black = (0, 0, 0)

# screen settings
WIDTH = 1200
HEIGHT = 700
mid_w = WIDTH // 2
mid_h = HEIGHT // 2
REL_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangular Assault")

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# fonts
game_text = pygame.font.SysFont('Arial', 72)
game_text_bold = pygame.font.SysFont('Arial Bold', 72)

# player
player_r = (
    (mid_w - REL_SIZE, mid_h - REL_SIZE),
    (mid_w + REL_SIZE // 2, mid_h),
    (mid_w - REL_SIZE, mid_h + REL_SIZE)
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_screen()
    update_screen()

pygame.quit()
sys.exit()
