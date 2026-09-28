import pygame as pg
WIDTH = 1024
HEIGHT = 768
TITLE = "Best game evah!!!"
TILESIZE = 32
FPS = 30

# colors
BGCOLOR = (137, 212, 84)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 139)
BLACK = (0, 0, 0)

# player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)