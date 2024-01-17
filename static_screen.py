import pygame
from screen_settings import screen, MID_W, MID_H, WIDTH, REL_SIZE
from styles import BLACK, WHITE, screen_font_bold, screen_font

pygame.init()


def draw_static_screen(li):
    # Covers game drawing
    screen.fill(BLACK, (0, MID_H - (REL_SIZE * 4), WIDTH, MID_H))
    # Title
    title_txt = 'GAME OVER' if li <= 0 else 'TRIANGULAR ASSAULT'
    title = screen_font_bold.render(title_txt, True, WHITE, BLACK)
    title_w = title.get_width()
    title_h = title.get_height()
    # Subtitle
    subtitle_txt = "To play again press 'space'" if li <= 0 else "To play press 'space'"
    subtitle = screen_font.render(subtitle_txt, True, WHITE, BLACK)
    subtitle_w = subtitle.get_width()
    # Draw title and subtitle
    screen.blit(title, (MID_W - title_w // 2, MID_H - title_h // 2))
    screen.blit(subtitle, (MID_W - subtitle_w // 2, MID_H + title_h // 2))
