import pygame
import random
import sys
import asyncio

pygame.init()
pygame.font.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen settings
WIDTH = 1200
HEIGHT = 700
MID_W = WIDTH // 2
MID_H = HEIGHT // 2
REL_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangular Assault")

# Fonts
hud_font = pygame.font.Font('assets/VCR_OSD_MONO_1.001.ttf', 40)
screen_font = pygame.font.SysFont('Arial', 30)
screen_font_bold = pygame.font.SysFont('Arial Bold', 120)

# Sound effects
hit_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
wave_sound_effect = pygame.mixer.Sound('assets/scoring-sound.wav')
damage_sound_effect = pygame.mixer.Sound('assets/explode.ogg')
shoot_sound_effect = pygame.mixer.Sound('assets/s2297_from_gd.ogg')

# Player
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

# Walls
topper = pygame.Rect(0, MID_H - (REL_SIZE * 4), WIDTH, REL_SIZE)
bottom = pygame.Rect(0, MID_H + (REL_SIZE * 3), WIDTH, REL_SIZE)

# Initial HUD stats
score = 0
life = 3
combo = 0
# waves
wave = 1
wave_start = True
wave_cooldown = 180
wave_timer = 0

# Variable trigger control
shot = False
bullets = []
bullet_radius = 10
move_left = False
shot_timer = 10
shot_delay = 90  # 1.5 sec at 60fps
miss = False
# shoot boundary
l_range = MID_W // 2
r_range = 3 * MID_W // 2
# game speed
mov_speed = 10
can_shoot = True


def handle_shoot():
    global bullets, shot_timer, shot_delay, miss, shot, can_shoot
    shot = False
    key = pygame.key.get_pressed()

    if key[pygame.K_a] or key[pygame.K_d]:
        player_position = player_l[1] if key[pygame.K_a] else player_r[1]
        # Checks if the last shot was more than 1.5 seconds ago or if the player pressed the keys quickly
        if shot_timer == 0 and can_shoot:
            shot = True
            direction_of_bullet = -1 if key[pygame.K_a] else 1
            initial_bul_pos = (player_position[0], player_position[1], direction_of_bullet)
            bullets.append(initial_bul_pos)
            if miss:
                miss = False
            shot_timer = 10
            shoot_sound_effect.play()
            can_shoot = False
    new_bullets = []
    for bullet in bullets:
        bx, by, dir = bullet
        bx += 3 * mov_speed * dir
        # checks collision with the left and right dashed line
        if l_range <= bx <= r_range:
            new_bullets.append((bx, by, dir))
    # Update the bullet
    bullets = new_bullets
    # Time
    if shot_timer > 0:
        shot_timer -= 1
    # handle key held
    if not (key[pygame.K_a] or key[pygame.K_d]):
        can_shoot = True


# Enemies
enemies = []
enemies_direction = []
wave_enemies = 4
spawned_enemies = 0
enemy_dimension = (2 * REL_SIZE, 2 * REL_SIZE)
spawn_delay = 120
spawn_delay_max = 60
spawn_timer = 0
enemy_speed_factor = 0


def handle_damage(player_dir, enemy, tp_en, tp_en_dir, i):
    global combo, life, enemies, enemies_direction
    if enemy.colliderect(pygame.draw.polygon(screen, WHITE, player_dir)):
        damage_sound_effect.play()
        combo = 0
        life -= 1
        tp_en.remove(enemy)
        tp_en_dir.pop(i)
        enemies = tp_en
        enemies_direction = tp_en_dir


def handle_enemies():
    global spawn_timer, spawned_enemies, enemies, enemies_direction
    global bullets, life, wave_start, miss, shot_timer, score, combo, wave_timer
    # Spawn enemies
    if spawned_enemies < wave_enemies:
        if spawn_timer == 0 and spawned_enemies <= wave_enemies:
            spawn_timer = spawn_delay
            spawned_enemies += 1
            side = random.randrange(-1, 2, 2)
            if side == 1:
                enemies.append(pygame.Rect((0 - enemy_dimension[0], MID_H - REL_SIZE), enemy_dimension))
            else:
                enemies.append(pygame.Rect((WIDTH, MID_H - REL_SIZE), enemy_dimension))
            enemies_direction.append(side)
    else:
        if wave_start and not enemies:
            wave_start = False
            wave_timer = wave_cooldown

    # Check collision
    temp_enemies = list(enemies)
    temp_enemies_direction = list(enemies_direction)
    temp_bullets = list(bullets)
    # collision with bullets
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0] - bullet_radius, bullet[1] - bullet_radius, bullet_radius, bullet_radius)
        collision = bullet_rect.collidelist(enemies)
        if collision != -1:
            hit_sound_effect.play()
            temp_bullets.remove(bullet)
            temp_enemies.pop(collision)
            temp_enemies_direction.pop(collision)
            score += int(10 * (1 + combo * 0.1))
            combo += 1
    enemies = temp_enemies
    enemies_direction = temp_enemies_direction
    bullets = temp_bullets
    # collision with player
    for enemy in enemies:
        index = enemies.index(enemy)
        if direction == 0:
            handle_damage(player_r, enemy, temp_enemies, temp_enemies_direction, index)
        else:
            handle_damage(player_l, enemy, temp_enemies, temp_enemies_direction, index)
    # Update enemy
    if wave_start:
        for enemy in enemies:
            enemy[0] += (mov_speed + enemy_speed_factor) * enemies_direction[enemies.index(enemy)]
            # check bullet miss
            if (enemy[0] + enemy[3] < MID_W // 2 or enemy[0] > 3 * MID_W // 2) and shot:
                miss = True
                shot_timer = 90
    # Spawn timer
    spawn_timer -= 1


def handle_waves():
    global wave_start, wave, wave_enemies, spawn_delay, spawned_enemies, wave_timer, enemy_speed_factor
    # Start a new wave if conditions are met
    if not wave_start:
        if wave_timer == 0:
            wave_start = True
            wave += 1
            if enemy_speed_factor <= 30:
                enemy_speed_factor += 2
            wave_enemies = 2 + wave * 2
            spawned_enemies = 0
            wave_sound_effect.play()
            if spawn_delay > spawn_delay_max:
                spawn_delay = 120 - (wave - 1) * 6
        else:
            wave_timer -= 1


def draw_game():
    screen.fill(BLACK)
    # Draw hud
    score_text = hud_font.render(f'SCORE: {score}', True, WHITE, BLACK)
    life_text = hud_font.render(f'LIFE: {life}', True, WHITE, BLACK)
    wave_text = hud_font.render(f'WAVE: {wave}', True, WHITE, BLACK)
    combo_text = hud_font.render(f'COMBO: {combo}', True, WHITE, BLACK)
    screen.blit(score_text, (20, 10))
    screen.blit(life_text, (WIDTH - 200, 10))
    screen.blit(combo_text, (20, 50))
    screen.blit(wave_text, (MID_W - 80, 10))

    if game_start:
        # Draw scenario
        pygame.draw.rect(screen, WHITE, topper)
        pygame.draw.rect(screen, WHITE, bottom)

        # Draw dotted lines
        start_y = MID_H - (REL_SIZE * 4)
        end_y = MID_H + (REL_SIZE * 3)
        dot_size = 10
        dot_space = 5
        y = start_y
        while y < end_y:
            pygame.draw.line(screen, WHITE, (MID_W // 2, y), (MID_W // 2, y + dot_size))
            pygame.draw.line(screen, WHITE, (3 * MID_W // 2, y), (3 * MID_W // 2, y + dot_size))
            y += dot_size + dot_space

        # Draw player
        if direction == 0:
            pygame.draw.polygon(screen, WHITE, player_r)
        else:
            pygame.draw.polygon(screen, WHITE, player_l)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), bullet_radius)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, WHITE, enemy)

    else:
        # Title
        title_txt = 'GAME OVER' if life <= 0 else 'TRIANGULAR ASSAULT'
        title = screen_font_bold.render(title_txt, True, WHITE, BLACK)
        title_w = title.get_width()
        title_h = title.get_height()

        # Subtitle
        subtitle_txt = "Not bad... Press 'start' to play again" if life <= 0 else "Press 'space' to play"
        subtitle = screen_font.render(subtitle_txt, True, WHITE, BLACK)
        subtitle_w = subtitle.get_width()

        # Draw title and subtitle
        screen.blit(title, (MID_W - title_w // 2, MID_H - title_h // 2))
        screen.blit(subtitle, (MID_W - subtitle_w // 2, MID_H + title_h // 2))


# Game stats
running = True
game_start = False
desired_direction = None


async def main():
    global running, game_start, score, combo, life, wave, desired_direction, direction
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif keys[pygame.K_SPACE]:
                if not game_start:
                    game_start = True
                    score = 0
                    combo = 0
                    wave = 1
                    life = 3

        if desired_direction is not None:
            direction = desired_direction

        if game_start:
            handle_shoot()
            handle_waves()
            if wave_start:
                handle_enemies()

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
        # Draw
        draw_game()

        # update screen
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
