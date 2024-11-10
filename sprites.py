import pygame as pg
from settings import *
vec = pg.math.Vector2

# ----------------------------- Player Class -----------------------------
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # กำหนดกลุ่มสไปร์ทที่ผู้เล่นจะถูกเพิ่มเข้าไป
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)  # เพิ่มตัว Player เข้ากลุ่มสไปร์ท
        self.game = game  # เก็บข้อมูลอ้างอิงถึงอ็อบเจกต์เกมหลัก
        self.image = pg.Surface((48, 48))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()  # สร้างสี่เหลี่ยมล้อมรอบพื้นผิว
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
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
        self.pos += self.vel * self.game.dt
        
        # Wrap around map boundaries
        if self.pos.x < 0:
            self.pos.x = (self.game.map.tilewidth - 1) * TILESIZE
        elif self.pos.x > (self.game.map.tilewidth - 1) * TILESIZE:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = (self.game.map.tileheight - 1) * TILESIZE
        elif self.pos.y > (self.game.map.tileheight - 1) * TILESIZE:
            self.pos.y = 0
        
        # อัปเดตตำแหน่งของผู้เล่นในกริดไปยังตำแหน่งจริงในพิกเซล
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

# ------------------------------------------------------------------------

# ------------------------------ Wall Class ------------------------------
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        # กำหนดกลุ่มสไปร์ทที่กำแพงจะถูกเพิ่มเข้าไป (ทั้ง all_sprites และ walls)
        self.groups = game.all_sprites, game.walls

        pg.sprite.Sprite.__init__(self, self.groups)    # เพิ่มตัว Wall เข้ากลุ่มสไปร์ท

        self.game = game    # เก็บข้อมูลอ้างอิงถึงอ็อบเจกต์เกมหลัก

        self.image = pg.Surface((TILESIZE, TILESIZE))   # สร้างพื้นผิวสี่เหลี่ยมขนาด 64 * 64 สำหรับกำแพง
        self.image.fill(GREEN)                          # และเติมสีเขียวให้กับพื้นผิวของกำแพง

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
        self.image.fill(RED)  # Initial color when visible
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
            self.image.fill(BLACK)  # Change color to blend with the background
            self.timer = 0
            # Remove from obstacles group so it no longer blocks the player
            self.game.obstacles.remove(self)
        elif not self.visible and self.timer >= self.disappear_time:
            self.visible = True
            self.image.fill(RED)  # Change back to visible color
            self.timer = 0
            # Add back to obstacles group so it blocks the player
            self.game.obstacles.add(self)