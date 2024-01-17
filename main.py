import pygame
import sys
import random
from styles import BLACK, WHITE
from screen_settings import screen, MID_W
from scenario import draw_lines, topper, bottom
from player import player_r, player_l, direction
from sfx import damage_sound_effect, shoot_sound_effect
from hud import draw_hud
from static_screen import draw_static_screen

# Initial HUD stats
score = 0
life = 3
wave = 0
combo = 0

# shoot boundary
l_range = MID_W // 2
r_range = MID_W + MID_W // 2

# Variable trigger controls for handle_shoot()
bullets = []
shot_timer = 0
shot_delay = 90  # 1.5 sec at 60fps
last_shot_time = 0


def update_screen():
    pygame.display.flip()
    pygame.time.Clock().tick(60)


def handle_shoot():
    global bullets, shot_timer, shot_delay, last_shot_time
    key = pygame.key.get_pressed()

    if (key[pygame.K_a] or key[pygame.K_d]) and shot_timer <= 0:
        current_time = pygame.time.get_ticks()
        # Checks if the last shot was more than 1.5 seconds ago or if the player pressed the keys quickly
        if current_time - last_shot_time >= shot_delay or shot_timer == 0:
            player_position = player_l[1] if key[pygame.K_a] else player_r[1]
            direction_of_bullet = -1 if key[pygame.K_a] else 1
            initial_bul_pos = (player_position[0], player_position[1], direction_of_bullet)
            bullets.append(initial_bul_pos)
            shot_timer = 90
            last_shot_time = current_time
            shoot_sound_effect.play()
    new_bullets = []
    for bullet in bullets:
        bx, by, dir = bullet
        bx += 5 * dir
        # checks collision with the left and right dashed line
        if l_range <= bx <= r_range:
            new_bullets.append((bx, by, dir))
    # Update the bullet
    bullets = new_bullets
    # Time
    if shot_timer > 0:
        shot_timer -= 1


def draw_game():
    screen.fill(BLACK)
    # Draw scenario
    pygame.draw.rect(screen, WHITE, topper)
    draw_lines()
    pygame.draw.rect(screen, WHITE, bottom)
    # Draw player
    if direction == 0:
        pygame.draw.polygon(screen, WHITE, player_r)
    else:
        pygame.draw.polygon(screen, WHITE, player_l)
    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 10)


# Game stats
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
        handle_shoot()
        # Player movement
        if keys[pygame.K_a]:
            desired_direction = 1
        elif keys[pygame.K_d]:
            desired_direction = 0
        else:
            desired_direction = None
        # Player death
        if life <= 0:
            game_start = False
            damage_sound_effect.play()
    elif life <= 0:
        draw_static_screen(life)
        if keys[pygame.K_SPACE]:
            # Reset stats
            score = combo = 0
            wave = 1
            life = 3
            game_start = True
    else:
        # Draw initial stats
        draw_static_screen(life)
        draw_hud(score, life, wave, combo)
    update_screen()

pygame.quit()
sys.exit()
