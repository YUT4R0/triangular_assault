from screen_settings import REL_SIZE, MID_H, MID_W

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
