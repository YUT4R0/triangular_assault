import pygame
import random
import sys

pygame.init()
pygame.font.init()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# screen settings
WIDTH = 1200
HEIGHT = 700
MID_W = WIDTH // 2
MID_H = HEIGHT // 2
REL_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangular Assault")
hud_font = pygame.font.Font('assets/VCR_OSD_MONO_1.001.ttf', 40)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/scoring-sound.wav')
die_sound_effect = pygame.mixer.Sound('assets/explode.ogg')

# fonts
game_text = pygame.font.SysFont('Arial', 72)
game_text_bold = pygame.font.SysFont('Arial Bold', 72)

# player
player_r = (
    (MID_W - REL_SIZE, MID_H - REL_SIZE),
    (MID_W + REL_SIZE // 2, MID_H),
    (MID_W - REL_SIZE, MID_H + REL_SIZE)
)
dir = 0

# score
score = 0
score_text = hud_font.render('SCORE: 0', True, WHITE, BLACK)

# lives
life = 3
life_text = hud_font.render('LIFE: 0', True, WHITE, BLACK)

# wave
wave = 1
wave_text = hud_font.render('WAVE: 1', True, WHITE, BLACK)

# combo
combo = 0
combo_text = hud_font.render('COMBO: 0', True, WHITE, BLACK)


def update_screen():
    pygame.display.flip()
    pygame.time.Clock().tick(60)


def draw_screen():
    screen.fill(BLACK)
    pygame.draw.polygon(screen, WHITE, player_r)
    screen.blit(score_text, (20, 10))
    screen.blit(life_text, (WIDTH - 200, 10))
    screen.blit(combo_text, (20, 50))
    screen.blit(wave_text, (MID_W - 80, 10))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # player movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            dir = 0
        elif event.key == pygame.K_d:
            dir = 1

    draw_screen()
    update_screen()

pygame.quit()
sys.exit()
