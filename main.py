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

# fonts
hud_font = pygame.font.Font('assets/VCR_OSD_MONO_1.001.ttf', 40)
screen_font = pygame.font.SysFont('Arial', 30)
screen_font_bold = pygame.font.SysFont('Arial Bold', 120)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/scoring-sound.wav')
death_sound_effect = pygame.mixer.Sound('assets/explode.ogg')

# player
direction = 0
player_r = (
    (MID_W - REL_SIZE, MID_H - REL_SIZE),
    (MID_W + REL_SIZE // 2, MID_H),
    (MID_W - REL_SIZE, MID_H + REL_SIZE)
)
player_l = (
    (MID_W + REL_SIZE, MID_H + REL_SIZE),
    (MID_W - REL_SIZE // 2, MID_H),
    (MID_W + REL_SIZE, MID_H - REL_SIZE)
)

# walls
topper = pygame.Rect(0, MID_H - (REL_SIZE * 4), WIDTH, REL_SIZE)
bottom = pygame.Rect(0, MID_H + (REL_SIZE * 3), WIDTH, REL_SIZE)

# initial hud stats
score = 0
life = 3
wave = 0
combo = 0

# variable trigger control
bullets = []
move_left = False
shot_timer = 0

def update_screen():
    pygame.display.flip()
    pygame.time.Clock().tick(60)


def draw_hud(n_score, n_life, n_wave, n_combo):
    score_text = hud_font.render(f'SCORE: {n_score}', True, WHITE, BLACK)
    life_text = hud_font.render(f'LIFE: {n_life}', True, WHITE, BLACK)
    wave_text = hud_font.render(f'WAVE: {n_wave}', True, WHITE, BLACK)
    combo_text = hud_font.render(f'COMBO: {n_combo}', True, WHITE, BLACK)
    screen.blit(score_text, (20, 10))
    screen.blit(life_text, (WIDTH - 200, 10))
    screen.blit(combo_text, (20, 50))
    screen.blit(wave_text, (MID_W - 80, 10))


def draw_static_screen(li):
    # covers game drawing
    screen.fill(BLACK, (0, MID_H - (REL_SIZE * 4), WIDTH, MID_H))
    # title
    title_txt = 'GAME OVER' if li <= 0 else 'TRIANGULAR ASSAULT'
    title = screen_font_bold.render(title_txt, True, WHITE, BLACK)
    title_w = title.get_width()
    title_h = title.get_height()

    # subtitle
    subtitle_txt = "To play again press 'space'" if li <= 0 else "To play press 'space'"
    subtitle = screen_font.render(subtitle_txt, True, WHITE, BLACK)
    subtitle_w = subtitle.get_width()

    # draw title and subtitle
    screen.blit(title, (MID_W - title_w // 2, MID_H - title_h // 2))
    screen.blit(subtitle, (MID_W - subtitle_w // 2, MID_H + title_h // 2))

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

def draw_game():
    screen.fill(BLACK)
    # draw scenario
    pygame.draw.rect(screen, WHITE, topper)
    draw_lines()
    pygame.draw.rect(screen, WHITE, bottom)
    # draw player
    if direction == 0:
        pygame.draw.polygon(screen, WHITE, player_r)
    else:
        pygame.draw.polygon(screen, WHITE, player_l)

def handle_shooting():
    global bullets, direction, score, life, combo, shot_timer

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_a] or keys[pygame.K_d]) and shot_timer <= 0:
        player_position = player_l[1] if keys[pygame.K_a] else player_r[1]
        direction_of_bullet = -1 if keys[pygame.K_a] else 1
        bullets.append((player_position[0], player_position[1], direction_of_bullet))
        scoring_sound_effect.play()
        shot_timer = 90  # 1,5 segundos a 60 FPS
    #time
    if shot_timer > 0:
        shot_timer -= 1

    # update posiotion bullet
    new_bullets = []
    for bullet in bullets:
        bx, by, dir = bullet
        bx += 5 * dir
        by = max(MID_H - (REL_SIZE * 4), min(MID_H + (REL_SIZE * 3), by))
        new_bullets.append((bx, by, dir))

    # remove bullet (ultrapassar a linha tracejada)
    bullets = [(bx, by, dir) for bx, by, dir in new_bullets if
               MID_H - (REL_SIZE * 4) <= by <= MID_H + (REL_SIZE * 3) and 0 < bx < WIDTH]

# game stats
running = True
game_start = False
desired_direction = None

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif keys[pygame.K_SPACE]:
            game_start = True

    if desired_direction is not None:
        direction = desired_direction

    if game_start:
        draw_game()
        wave = 1
        draw_hud(score, life, wave, combo)
        handle_shooting()

        new_bullets = []
        for bullet in bullets:
            if 0 < bullet[0] < WIDTH:
                bullet_y = max(MID_H - (REL_SIZE * 4), min(MID_H + (REL_SIZE * 3), bullet[1]))
                if MID_H - (REL_SIZE * 4) <= bullet_y <= MID_H + (REL_SIZE * 3):
                    pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet_y)), 5)
                    new_bullets.append((bullet[0], bullet_y, bullet[2]))
        bullets = new_bullets


        #movement
        if keys[pygame.K_a]:
            desired_direction = 1
        elif keys[pygame.K_d]:
            desired_direction = 0
        else:
            desired_direction = None

        # player's death
        if life <= 0:
            game_start = False
            death_sound_effect.play()

    elif life <= 0:
        draw_static_screen(life)
        if keys[pygame.K_SPACE]:
            # reset stats
            score = combo = 0
            wave = 1
            life = 3
            game_start = True
    else:
        # draws initial stats
        draw_static_screen(life)
        draw_hud(score, life, wave, combo)
    update_screen()

pygame.quit()
sys.exit()
