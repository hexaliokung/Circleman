import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

# ----------------------------- Player Class -----------------------------
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)  # เรียกใช้ constructor ของ Sprite โดยตรง
        # existing code
        self.game = game
        self.image = pg.Surface(((TILESIZE // 4) * 3, (TILESIZE // 4) * 3))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.speed_boost = False
        self.boost_timer = 0
        self.boost_time = 5000  # Default boost time of 5 seconds

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        # ถ้ามีการเพิ่มความเร็ว (speed boost) ให้ตัวละครเคลื่อนที่เร็วขึ้น
        speed = PLAYER_SPEED * 1.5 if self.speed_boost else PLAYER_SPEED  # ถ้ากำลังมีความเร็วเพิ่มจะวิ่งเร็วขึ้น
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = speed
        
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def move(self, dx=0, dy=0):
        # ฟังก์ชันเคลื่อนที่ตามค่าที่ส่งเข้ามา ถ้าไม่ชนกับกำแพง
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dir):
        # Check for collisions with both walls and visible obstacles
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False) or \
                   pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False) or \
                   pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                    
    def update(self):
        self.get_keys()
        if self.speed_boost:
            # เพิ่มความเร็วเมื่อมี speed_boost
            self.vel = self.vel * 1.5  # เพิ่มตัวคูณความเร็ว
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls("x")

        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        # ลดเวลา speed_boost ลง
        if self.speed_boost:
            self.boost_timer += self.game.dt * 1000  # คำนวณเวลาเพิ่มในมิลลิวินาที
            if self.boost_timer >= self.boost_time:
                self.speed_boost = False  # ปิด speed_boost เมื่อหมดเวลา
                self.boost_timer = 0  # รีเซ็ต timer


        # อัปเดตการ wrap ของตำแหน่งผู้เล่นในแผนที่
        if self.pos.x < 0:
            self.pos.x = (self.game.map.tilewidth - 1) * TILESIZE
        elif self.pos.x > (self.game.map.tilewidth - 1) * TILESIZE:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = (self.game.map.tileheight - 1) * TILESIZE
        elif self.pos.y > (self.game.map.tileheight - 1) * TILESIZE:
            self.pos.y = 0

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
# ------------------------------------------------------------------------

# ------------------------------ Wall Class ------------------------------
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        # กำหนดกลุ่มสไปร์ทที่กำแพงจะถูกเพิ่มเข้าไป (ทั้ง all_sprites และ walls)
        self.groups = game.all_sprites, game.walls

        pg.sprite.Sprite.__init__(self, self.groups)    # เพิ่มตัว Wall เข้ากลุ่มสไปร์ท

        self.game = game    # เก็บข้อมูลอ้างอิงถึงอ็อบเจกต์เกมหลัก

        self.image = pg.Surface((TILESIZE, TILESIZE))   # สร้างพื้นผิวสี่เหลี่ยมขนาด 64 * 64 สำหรับกำแพง
        self.image.fill(BLACK)                          # และเติมสีเขียวให้กับพื้นผิวของกำแพง

        self.rect = self.image.get_rect()   # สร้างสี่เหลี่ยมล้อมรอบพื้นผิวเพื่อใช้งานหลายอย่างเช่น การตรวจจับการชนของวัตถุ

        self.x = x  # ตำแหน่ง X ของกำแพงในกริด
        self.y = y  # ตำแหน่ง Y ของกำแพงในกริด

        # อัปเดตตำแหน่งกำแพงในพิกเซลโดยคูณตำแหน่งในกริดด้วยขนาด TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
# ------------------------------------------------------------------------

class TimedObstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, appear_time=2000, disappear_time=2000):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)  # Initial color when visible
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
        self.appear_time = appear_time
        self.disappear_time = disappear_time
        self.timer = 0
        self.visible = True

    def update(self):
        # Update timer for visibility toggle
        self.timer += self.game.dt * 1000  # Convert dt to milliseconds

        # Toggle visibility and adjust collision based on visibility
        if self.visible and self.timer >= self.appear_time:
            self.visible = False
            self.image.set_alpha(0)  # Make it invisible (transparent)
            self.timer = 0
            # Remove from obstacles group so it no longer blocks the player
            self.game.obstacles.remove(self)
        elif not self.visible and self.timer >= self.disappear_time:
            self.visible = True
            self.image.set_alpha(255)  # Make it visible with BLACK color
            self.image.fill(BLACK)     # Ensure it is black when visible
            self.timer = 0
            # Add back to obstacles group so it blocks the player
            self.game.obstacles.add(self)
# ------------------------------------------------------------------------
# Fruit class
class Fruit(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.fruits  # fruits group for collision detection
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # สร้างพื้นผิวสี่เหลี่ยมที่มีขนาดเท่ากับ TILESIZE
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)  # เปิดใช้งานพื้นหลังว่างเปล่า
        self.rect = self.image.get_rect()
        
        # ขนาดของวงกลมที่เล็กลงและตั้งตำแหน่งตรงกลางของ TILESIZE
        small_radius = TILESIZE // 4
        pg.draw.circle(self.image, GREEN1, (TILESIZE // 2, TILESIZE // 2), small_radius)

        # ตั้งค่าตำแหน่งของผลไม้ในกริด
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class SpecialFruit(Fruit):
    def __init__(self, game, x, y):
        # เรียกใช้ constructor ของ Fruit
        super().__init__(game, x, y)
        
        # เปลี่ยนสีผลไม้พิเศษให้แตกต่างจากผลไม้ปกติ
        self.image.fill(RED)  # ใช้สีที่แตกต่าง เช่น สีแดง
        self.rect = self.image.get_rect()
        
        # ตั้งตำแหน่ง
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        # สุ่มระยะเวลาเพิ่มความเร็ว (เพิ่มความเร็ว 5 วินาที)
        self.boost_time = 5000  # 5 วินาที
