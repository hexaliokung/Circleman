import pygame as pg
import random
from settings import *
vec = pg.math.Vector2
# Tle and Iya
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)  # เรียกใช้ constructor ของ Sprite โดยตรง
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

        # ปรับตัวคูณความเร็วตาม speed_multiplier
        speed = PLAYER_SPEED * (self.speed_multiplier if self.speed_boost else 1)
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


        # หลุดแผนที่ย้ายไปทิศตรงข้าม
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

# Tle
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

# Tle
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

# Iya
class Fruit(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        # เพิ่มเข้าสู่กลุ่มที่ใช้การตรวจจับการชนและการแสดงผล
        self.groups = game.all_sprites, game.fruits # เพิ่มผลไม้ เข้ากลุ่มวัตถุของเกม และกลุ่มวัตถุของผลไม้
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        # สร้างหน้าตาให้เป็ฯสี่เหลี่ยมขนาดเท่า TILESIZE และเปิดใช้งานพื้นหลังโปร่งใส
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)

        # สร้างกรอบสี่เหลี่ยมเพื่อตรวจจับการชน
        self.rect = self.image.get_rect()

        # รัศมีของวงกลมคือ 1 ใน 4 ของขนาด TILESIZE
        small_radius = TILESIZE // 4

        # วาดวงกลมสีเขียวอยู่ตรงกลางของ TILESIZE โดยมีขนาดรัสมี = small_radius
        pg.draw.circle(self.image, GREEN1, (TILESIZE // 2, TILESIZE // 2), small_radius)

        # ตั้งค่าตำแหน่งของผลไม้ให้ตรงกับตำแหน่งในแผนที่
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Iya class SpecialFruit เป็นคลาสลูกของ class Fruit
class SpecialFruit(Fruit):
    def __init__(self, game, x, y):
        # เรียกใช้ constructor ของ Class Fruit
        super().__init__(game, x, y)

        self.image.fill((0, 0, 0, 0))  # ล้างพื้นหลังให้โปร่งใส

        # เปลี่ยนสีของวงกลมเป็นสีแดง และมีขนาด ใหญ่ขึ้นเล็กน้อย
        pg.draw.circle(self.image, RED, (TILESIZE // 2, TILESIZE // 2), TILESIZE // 3)

        # สุ่มเอฟเฟกต์เป็นเพิ่มหรือลดความเร็ว
        self.effect_type = random.choice(["speed_up", "speed_down"])
        self.boost_time = 5000  # ระยะเวลาผลของเอฟเฟกต์ 5 วินาที

    def apply_effect(self, player):
        if self.effect_type == "speed_up":
            player.speed_boost = True
            player.boost_timer = 0
            player.speed_multiplier = 1.5  # เพิ่มความเร็ว
        elif self.effect_type == "speed_down":
            player.speed_boost = True
            player.boost_timer = 0
            player.speed_multiplier = 0.5  # ลดความเร็ว

# Pao
class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y, image, color, speed):
        super().__init__()
        self.game = game
        self.image = image
        self.color = color
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE  # ใช้ vec สำหรับการคำนวณตำแหน่ง
        self.speed = speed / 2  # ปรับความเร็วให้ช้าลง (อาจปรับค่าตามต้องการ)
        self.health = 100

    def update(self):
        self.draw_health_bar()
        self.follow_player(self.game.player)
        self.rect.topleft = self.pos  # อัปเดตตำแหน่งตาม `pos`
    
    def follow_player(self, player):
        """ทำให้ผีเคลื่อนที่ไปหาผู้เล่นและตรวจสอบการชนกำแพง"""
        direction = vec(0, 0)
        
        # คำนวณทิศทางที่ผีจะเคลื่อนไปหาผู้เล่น
        if self.pos.x < player.pos.x:
            direction.x = self.speed
        elif self.pos.x > player.pos.x:
            direction.x = -self.speed
        if self.pos.y < player.pos.y:
            direction.y = self.speed
        elif self.pos.y > player.pos.y:
            direction.y = -self.speed


    def draw_health_bar(self):#แสดงแถบพลังชีวิตของผี
        bar_width = 50
        bar_height = 5
        fill = (self.health / 100) * bar_width
        bar = pg.Rect(self.rect.x, self.rect.y - 10, bar_width, bar_height)
        fill_rect = pg.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
    
        # วาดแถบพลังชีวิต
        pg.draw.rect(self.game.scr_display, (255, 0, 0), bar)  # ใช้ self.game.scr_display แทน self.game.screen
        pg.draw.rect(self.game.scr_display, (0, 255, 0), fill_rect)  # ใช้ self.game.scr_display แทน self.game.screen



    def take_damage(self, amount):
        """ลดพลังชีวิตของผี"""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """ทำให้ผีตาย"""
        self.kill()

# Pao
class Blinky(Ghost):
    def __init__(self, game, x, y):  # ผีแดง
        blinky_img = pg.transform.scale(pg.image.load('img/red.png'), (TILESIZE, TILESIZE))
        super().__init__(game, x, y, blinky_img, "red", speed=2)

    def update(self):
        self.follow_player(self.game.player)  # ทำให้ผีบลินกี้ตามผู้เล่น
        super().update()  # เรียกใช้การอัปเดตจากคลาสแม่ (ตรวจสอบแถบพลังชีวิต)

# Pao
class Pinky(Ghost):
    def __init__(self, game, x, y):  # ผีชมพู
        pinky_img = pg.transform.scale(pg.image.load('img/pink.png'), (TILESIZE, TILESIZE))
        super().__init__(game, x, y, pinky_img, "pink", speed=2)

    def update(self):
        self.follow_player(self.game.player)  # ทำให้ผีพิงกี้ตามผู้เล่น
        super().update()  # เรียกใช้การอัปเดตจากคลาสแม่ (ตรวจสอบแถบพลังชีวิต)

# Pao
class Inky(Ghost):
    def __init__(self, game, x, y): # ผีฟ้า

        inky_img = pg.transform.scale(pg.image.load('img/blue.png'), (TILESIZE, TILESIZE))
        super().__init__(game, x, y, inky_img, "blue", speed=2)

    def update(self):
        self.follow_player(self.game.player)  # ทำให้ผีอินกี้ตามผู้เล่น
        super().update()  # เรียกใช้การอัปเดตจากคลาสแม่ (ตรวจสอบแถบพลังชีวิต)

# Pao
class Clyde(Ghost):
    def __init__(self, game, x, y):  # ผีส้ม
        clyde_img = pg.transform.scale(pg.image.load('img/orange.png'), (TILESIZE, TILESIZE))
        super().__init__(game, x, y, clyde_img, "orange", speed=2)

    def update(self):
        self.follow_player(self.game.player)  # ทำให้ผีคลายด์ตามผู้เล่น
        super().update()  # เรียกใช้การอัปเดตจากคลาสแม่ (ตรวจสอบแถบพลังชีวิต)