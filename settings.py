import pygame as pg
from pygame.math import Vector2 as vec

# สีต่างๆ (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (30, 30, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
GREEN1 = (173, 255, 47)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# game settings
WIDTH = 1600   # 16 * 100 or 32 * 50 or 64 * 25
HEIGHT = 960  # 16 * 60 or 32 * 30 or 64 * 15
FPS = 60

TILESIZE = 40
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 250
PLAYER_IMG = "betty.png"

# ขนาดของ TILESIZE ที่ใช้ใน settings.py
from settings import TILESIZE

# โหลดและปรับขนาดภาพผีทั้ง 4 ตัว
blinky_img = pg.transform.scale(pg.image.load('img/red.png'), (TILESIZE, TILESIZE))
pinky_img = pg.transform.scale(pg.image.load('img/pink.png'), (TILESIZE, TILESIZE))
inky_img = pg.transform.scale(pg.image.load('img/blue.png'), (TILESIZE, TILESIZE))
clyde_img = pg.transform.scale(pg.image.load('img/orange.png'), (TILESIZE, TILESIZE))