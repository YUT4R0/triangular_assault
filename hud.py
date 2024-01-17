import pygame
from styles import hud_font, WHITE, BLACK
from screen_settings import screen, WIDTH, MID_W

pygame.init()


def draw_hud(n_score, n_life, n_wave, n_combo):
    score_text = hud_font.render(f'SCORE: {n_score}', True, WHITE, BLACK)
    life_text = hud_font.render(f'LIFE: {n_life}', True, WHITE, BLACK)
    wave_text = hud_font.render(f'WAVE: {n_wave}', True, WHITE, BLACK)
    combo_text = hud_font.render(f'COMBO: {n_combo}', True, WHITE, BLACK)
    screen.blit(score_text, (20, 10))
    screen.blit(life_text, (WIDTH - 200, 10))
    screen.blit(combo_text, (20, 50))
    screen.blit(wave_text, (MID_W - 80, 10))
