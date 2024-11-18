# settings.py make by Tle

import pygame as pg
from pygame.math import Vector2 as vec  # ใช้ Vector2 สำหรับการจัดการตำแหน่งและการเคลื่อนที่

# สีต่างๆ ในรูปแบบ RGB (Red, Green, Blue)
WHITE = (255, 255, 255)      # สีขาว
BLACK = (0, 0, 0)            # สีดำ
DARKGREY = (30, 30, 40)      # สีเทาเข้ม
LIGHTGREY = (100, 100, 100)  # สีเทาอ่อน
GREEN = (0, 255, 0)          # สีเขียว
GREEN1 = (173, 255, 47)      # สีเขียวอ่อน
RED = (255, 0, 0)            # สีแดง
YELLOW = (255, 255, 0)       # สีเหลือง
ORANGE = (255, 165, 0)       # สีส้ม

# การตั้งค่าพื้นฐานของเกม
WIDTH = 1600   # ความกว้างของหน้าจอเกม
HEIGHT = 960   # ความสูงของหน้าจอเกม
FPS = 60       # จำนวนเฟรมต่อวินาที (Frames Per Second)

# ขนาดของแต่ละ TILE (ช่องในกริด)
TILESIZE = 40  # ขนาดของ TILE ในหน่วยพิกเซล

# คำนวณจำนวน TILE ในแนวนอนและแนวตั้งของกริด
GRIDWIDTH = WIDTH / TILESIZE  # จำนวน TILE ในแนวนอน
GRIDHEIGHT = HEIGHT / TILESIZE  # จำนวน TILE ในแนวตั้ง

# การตั้งค่าผู้เล่น
PLAYER_SPEED = 250  # ความเร็วของตัวผู้เล่น (ในหน่วยพิกเซลต่อวินาที)

# ขนาดของ TILESIZE ที่ใช้ใน settings.py
from settings import TILESIZE  # นำเข้าค่าขนาด TILE จาก settings.py

# โหลดและปรับขนาดภาพผีแต่ละตัว
# blinky_img, pinky_img, inky_img, clyde_img คือ sprite ของผีแต่ละชนิดที่ถูกโหลดและปรับขนาด
blinky_img = pg.transform.scale(pg.image.load('img/red1.png'), (TILESIZE, TILESIZE))  # โหลดรูป Blinky (ผีแดง) และปรับขนาดให้เท่ากับ TILESIZE
pinky_img = pg.transform.scale(pg.image.load('img/pink.png'), (TILESIZE, TILESIZE))  # โหลดรูป Pinky (ผีชมพู) และปรับขนาดให้เท่ากับ TILESIZE
inky_img = pg.transform.scale(pg.image.load('img/blue.png'), (TILESIZE, TILESIZE))   # โหลดรูป Inky (ผีฟ้า) และปรับขนาดให้เท่ากับ TILESIZE
clyde_img = pg.transform.scale(pg.image.load('img/orange.png'), (TILESIZE, TILESIZE)) # โหลดรูป Clyde (ผีส้ม) และปรับขนาดให้เท่ากับ TILESIZE