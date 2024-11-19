import pygame as pg  # นำเข้าโมดูล Pygame สำหรับจัดการเกม
import random  # ใช้สำหรับการสุ่มค่า
import heapq  # ใช้สำหรับอัลกอริทึม A* Pathfinding

from settings import *  # นำเข้าการตั้งค่าจากไฟล์ settings.py
vec = pg.math.Vector2  # ใช้ Vector2 สำหรับการคำนวณตำแหน่งและการเคลื่อนที่

# ====================
# Player Class (Tle, Iya, Tin)
# ====================
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        """
        สร้างตัวละครผู้เล่นและกำหนดคุณสมบัติต่าง ๆ เช่น ตำแหน่ง ความเร็ว และชีวิต
        """
        pg.sprite.Sprite.__init__(self, game.all_sprites)  # เพิ่มผู้เล่นในกลุ่ม sprite
        self.game = game  # เชื่อมโยงกับเกมหลัก

        # สร้างภาพตัวละคร
        self.image = pg.Surface(((TILESIZE // 4) * 3, (TILESIZE // 4) * 3))
        self.image = pg.image.load("img/player.png").convert_alpha()  # โหลดภาพผู้เล่น
        self.rect = self.image.get_rect()  # สร้างสี่เหลี่ยมรอบภาพสำหรับการชนกัน

        # กำหนดความเร็วและตำแหน่ง
        self.vel = vec(0, 0)  # ความเร็วเริ่มต้น
        self.pos = vec(x, y) * TILESIZE  # ตำแหน่งเริ่มต้นในหน่วย Tile

        # คุณสมบัติเกี่ยวกับ Boost
        self.speed_boost = False
        self.boost_timer = 0
        self.boost_time = 5000  # เวลาของ Boost (5 วินาที)

        # กำหนดชีวิตและสถานะ
        self.lives = 3
        self.alive = True

    def get_keys(self):
        """
        รับการกดปุ่มคีย์บอร์ดและกำหนดทิศทางการเคลื่อนที่ของผู้เล่น
        """
        self.vel = vec(0, 0)  # ตั้งค่าความเร็วเริ่มต้น
        keys = pg.key.get_pressed()  # รับคีย์ที่ถูกกด

        # กำหนดความเร็วตาม Boost
        speed = PLAYER_SPEED * (self.speed_multiplier if self.speed_boost else 1)

        # ตรวจสอบการกดปุ่มเพื่อกำหนดทิศทาง
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = speed

        # ลดความเร็วเมื่อเคลื่อนที่แนวทแยง
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def move(self, dx=0, dy=0):
        """
        ย้ายตำแหน่งผู้เล่นโดยตรวจสอบว่าชนกำแพงหรือไม่
        """
        if not self.collide_with_walls(dx, dy):  # ถ้าไม่ชนกำแพง
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dir):
        """
        ตรวจสอบการชนกับกำแพงหรือวัตถุในทิศทางที่กำหนด
        """
        if dir == "x":  # ตรวจสอบการชนในแกน X
            hits = pg.sprite.spritecollide(self, self.game.walls, False) or \
                   pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vel.x > 0:  # ถ้าเคลื่อนที่ไปทางขวา
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:  # ถ้าเคลื่อนที่ไปทางซ้าย
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == "y":  # ตรวจสอบการชนในแกน Y
            hits = pg.sprite.spritecollide(self, self.game.walls, False) or \
                   pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vel.y > 0:  # ถ้าเคลื่อนที่ลง
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:  # ถ้าเคลื่อนที่ขึ้น
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                    
    def update(self):
        """
        อัปเดตตำแหน่งและสถานะของผู้เล่น
        """
        self.get_keys()  # รับคีย์จากผู้เล่น
        self.pos += self.vel * self.game.dt  # คำนวณตำแหน่งใหม่

        # ตรวจสอบการชน
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        # ตรวจสอบสถานะ Boost
        if self.speed_boost:
            self.boost_timer += self.game.dt * 1000
            if self.boost_timer >= self.boost_time:
                self.speed_boost = False  # หมดเวลาของ Boost
                self.boost_timer = 0

        # วาร์ปผู้เล่นเมื่อหลุดขอบแผนที่
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

    def take_damage(self):
        """
        ลดจำนวนชีวิตเมื่อผู้เล่นถูกโจมตี
        """
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.alive = False
            self.game.player_died()  # เรียกฟังก์ชันเมื่อผู้เล่นตาย

    def respawn(self, x, y):
        """
        คืนชีพผู้เล่นที่ตำแหน่งใหม่
        """
        self.alive = True
        self.pos = vec(x, y) * TILESIZE
        self.rect.topleft = self.pos
        self.vel = vec(0, 0)

# Tle
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        """
        กำหนดคุณสมบัติของกำแพงในแผนที่
        """
        self.groups = game.all_sprites, game.walls  # กำหนดให้กำแพงอยู่ในกลุ่ม sprites ทั้งหมดและกลุ่ม walls
        pg.sprite.Sprite.__init__(self, self.groups)  # เพิ่มวัตถุ Wall ลงในกลุ่ม

        self.game = game  # อ้างอิงถึงอ็อบเจกต์เกมหลัก

        # สร้างพื้นผิวสำหรับกำแพงและกำหนดสี
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)

        # สร้างพื้นที่สี่เหลี่ยมที่กำหนดตำแหน่งของกำแพง
        self.rect = self.image.get_rect()
        self.x = x  # ตำแหน่ง x ในตารางแผนที่
        self.y = y  # ตำแหน่ง y ในตารางแผนที่

        # อัปเดตตำแหน่งจริงในหน่วยพิกเซล
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Tle
class TimedObstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, appear_time=2000, disappear_time=2000, start_time=0):
        """
        สร้างวัตถุสิ่งกีดขวางที่ปรากฏและหายไปตามเวลา
        """
        self.groups = game.all_sprites, game.obstacles  # อยู่ในกลุ่มวัตถุทั้งหมดและกลุ่ม obstacles
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game  # อ้างอิงถึงเกมหลัก

        # สร้างพื้นผิวสำหรับสิ่งกีดขวาง
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)  # ตั้งสีดำสำหรับพื้นหลังสิ่งกีดขวาง
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        # ตั้งค่าความถี่ในการปรากฏและหายไป
        self.appear_time = appear_time
        self.disappear_time = disappear_time
        self.start_time = start_time
        self.timer = -self.start_time  # ตัวจับเวลาเริ่มต้น
        self.visible = False  # เริ่มต้นในสถานะที่มองไม่เห็น

    def update(self):
        """
        อัปเดตสถานะของสิ่งกีดขวางตามเวลา
        """
        self.timer += self.game.dt * 1000  # เพิ่มค่าเวลาในหน่วยมิลลิวินาที

        # ถ้าถึงเวลาที่สิ่งกีดขวางควรปรากฏ/หายไป
        if self.timer >= 0:
            if self.visible and self.timer >= self.appear_time:
                self.visible = False
                self.image.set_alpha(0)  # ทำให้โปร่งใส
                self.timer = 0  # รีเซ็ตตัวจับเวลา
                self.game.obstacles.remove(self)  # ลบออกจากกลุ่ม obstacles

            elif not self.visible and self.timer >= self.disappear_time:
                self.visible = True
                self.image.set_alpha(255)  # แสดงสิ่งกีดขวาง
                self.image.fill(BLACK)
                self.timer = 0  # รีเซ็ตตัวจับเวลา
                self.game.obstacles.add(self)  # เพิ่มกลับในกลุ่ม obstacles

# Tle
class TimedTrap(pg.sprite.Sprite):
    def __init__(self, game, x, y, appear_time=5000, disappear_time=3500):
        """
        สร้างกับดักที่สามารถปรากฏ/หายไปได้ตามเวลา
        """
        self.groups = game.all_sprites, game.traps  # อยู่ในกลุ่ม traps
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game  # อ้างอิงถึงเกมหลัก
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)  # ใช้สีแดงแทนกับดัก
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        # ตั้งค่าเวลาปรากฏและหายไป
        self.appear_time = appear_time
        self.disappear_time = disappear_time
        self.timer = 0  # เริ่มต้นตัวจับเวลา
        self.visible = True  # เริ่มต้นให้มองเห็น

    def update(self):
        """
        อัปเดตสถานะของกับดักตามเวลา
        """
        self.timer += self.game.dt * 1000  # เพิ่มค่าเวลาในหน่วยมิลลิวินาที

        # สลับสถานะการแสดงผลเมื่อถึงเวลา
        if self.visible and self.timer >= self.appear_time:
            self.visible = False
            self.image.set_alpha(0)  # ทำให้โปร่งใส
            self.timer = 0  # รีเซ็ตตัวจับเวลา
        elif not self.visible and self.timer >= self.disappear_time:
            self.visible = True
            self.image.set_alpha(255)  # ทำให้มองเห็นได้
            self.timer = 0  # รีเซ็ตตัวจับเวลา

    def on_player_collide(self, player):
        """
        ลดชีวิตผู้เล่นเมื่อชนกับดัก
        """
        if self.visible:  # ถ้ากับดักกำลังแสดงผล
            player.take_damage()  # ลดชีวิตของผู้เล่น
            if player.lives > 0:
                self.game.reset_positions()  # รีเซ็ตตำแหน่งผู้เล่น
            self.game.boom.play()  # เล่นเสียงระเบิด

# Iya
class Fruit(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        """
        สร้างผลไม้ที่ผู้เล่นสามารถเก็บได้
        """
        self.groups = game.all_sprites, game.fruits  # เพิ่มไปในกลุ่ม fruits
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game  # อ้างอิงถึงเกมหลัก

        # สร้างพื้นผิวสำหรับผลไม้
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        self.rect = self.image.get_rect()

        # วาดวงกลมแสดงผลไม้
        small_radius = TILESIZE // 4
        pg.draw.circle(self.image, GREEN1, (TILESIZE // 2, TILESIZE // 2), small_radius)

        # ตั้งตำแหน่งผลไม้
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Iya class SpecialFruit เป็นคลาสลูกของ class Fruit
class SpecialFruit(Fruit):
    def __init__(self, game, x, y):
        """
        สร้างผลไม้พิเศษที่มอบเอฟเฟกต์พิเศษแก่ผู้เล่น
        """
        super().__init__(game, x, y)  # เรียกใช้งานจากคลาส Fruit

        # เปลี่ยนสีและลักษณะของผลไม้พิเศษ
        self.image.fill((0, 0, 0, 0))  # ตั้งค่าโปร่งใส
        pg.draw.circle(self.image, RED, (TILESIZE // 2, TILESIZE // 2), TILESIZE // 3)

        # เลือกเอฟเฟกต์พิเศษแบบสุ่ม
        self.effect_type = random.choice(["speed_up", "speed_down", "ghost_speed_up", "ghost_speed_down"])
        self.boost_time = 5000  # ระยะเวลาของเอฟเฟกต์

    def apply_effect(self, game):
        if self.effect_type == "speed_up":
            # เพิ่มความเร็วให้ผู้เล่น
            game.player.speed_boost = True
            game.player.boost_timer = 0
            game.player.speed_multiplier = 1.2  # เพิ่มความเร็วผู้เล่น 20%
        elif self.effect_type == "speed_down":
            # ลดความเร็วผู้เล่น
            game.player.speed_boost = True
            game.player.boost_timer = 0
            game.player.speed_multiplier = 0.9  # ลดความเร็วผู้เล่น 10%
        elif self.effect_type == "ghost_speed_up":
            # เพิ่มความเร็วให้กับผี
            game.apply_ghost_speed_effect(multiplier=1.5, duration=self.boost_time)
        elif self.effect_type == "ghost_speed_down":
            # ลดความเร็วให้กับผี
            game.apply_ghost_speed_effect(multiplier=0.5, duration=self.boost_time)

# Pao
class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y, image, color, speed):
        super().__init__()
        self.game = game
        self.image = image
        self.color = color
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE  # ตำแหน่งปัจจุบันในรูปแบบ Vector2
        self.target = self.pos  # ตำแหน่งเป้าหมายเริ่มต้น
        self.speed = speed  # ความเร็วในการเคลื่อนที่ของผี
        self.pathfinding_timer = 0  # ตัวจับเวลาเพื่อลดความถี่การเรียก A*

    def update(self):
        """อัปเดตตำแหน่งของผี"""
        # ลดความถี่ในการอัปเดตเป้าหมาย
        self.pathfinding_timer += self.game.dt * 1000
        if self.pathfinding_timer > 500:  # อัปเดตเป้าหมายทุก 500 มิลลิวินาที
            self.target = self.get_next_target()
            self.pathfinding_timer = 0

        # คำนวณการเคลื่อนที่
        if self.pos.distance_to(self.target) <= self.speed * self.game.dt:
            self.pos = self.target
        else:
            direction = (self.target - self.pos).normalize()
            if direction.length() > 0:
                self.pos += direction * self.speed * self.game.dt

        self.rect.center = self.pos
    
    def follow_player(self, player):
        """ทำให้ผีเคลื่อนที่เข้าหาผู้เล่น"""
        direction = vec(0, 0)

        # คำนวณทิศทางที่ผีควรเคลื่อนไป
        if self.pos.x < player.pos.x:
            direction.x = self.speed
        elif self.pos.x > player.pos.x:
            direction.x = -self.speed
        if self.pos.y < player.pos.y:
            direction.y = self.speed
        elif self.pos.y > player.pos.y:
            direction.y = -self.speed

        # อัปเดตตำแหน่งของผี
        self.pos += direction * self.game.dt

    def random_move(self):
        """ทำให้ผีเคลื่อนไหวแบบสุ่ม"""
        self.random_timer += self.game.dt  # เพิ่มเวลา

        # เปลี่ยนทิศทางทุก 2 วินาที
        if self.random_timer >= 2:
            self.random_dir = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.random_timer = 0  # รีเซ็ตเวลา

        # เคลื่อนที่ในทิศทางปัจจุบัน
        direction = vec(self.random_dir[0], self.random_dir[1]) * self.speed
        self.pos += direction * self.game.dt

    def astar_pathfinding(self, start, goal):
        """A* Pathfinding"""
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                # สร้างเส้นทางจาก start -> goal
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_list]:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        # ถ้าไม่มีเส้นทาง
        return None

    def heuristic(self, a, b):
        """คำนวณระยะทาง Manhattan"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        """ค้นหาตำแหน่งที่เพื่อนบ้านสามารถไปได้"""
        neighbors = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]
        # กรองเพื่อนบ้านที่ไม่ชนกำแพง
        valid_neighbors = [n for n in neighbors if self.is_valid_position(n)]
        return valid_neighbors

    def is_valid_position(self, pos):
        """ตรวจสอบว่าตำแหน่งสามารถเดินได้ (ไม่ชนกำแพง)"""
        x, y = pos
        return 0 <= x < self.game.map.tilewidth and 0 <= y < self.game.map.tileheight and not self.game.is_wall(x, y)

    def get_next_target(self):
        """กำหนดตำแหน่งเป้าหมายใหม่"""
        start = (int(self.pos.x // TILESIZE), int(self.pos.y // TILESIZE))
        goal = (int(self.game.player.pos.x // TILESIZE), int(self.game.player.pos.y // TILESIZE))
        path = self.astar_pathfinding(start, goal)

        if path:  # หากมีเส้นทาง
            next_tile = path[0]
            return vec(next_tile[0] * TILESIZE + TILESIZE // 2, next_tile[1] * TILESIZE + TILESIZE // 2)
        
        # กรณีไม่มีเส้นทาง ให้สุ่มตำแหน่งใหม่ในพื้นที่ใกล้เคียง
        neighbors = self.get_neighbors(start)
        if neighbors:
            random_tile = random.choice(neighbors)
            return vec(random_tile[0] * TILESIZE + TILESIZE // 2, random_tile[1] * TILESIZE + TILESIZE // 2)
        
        # ถ้าไม่มีทางเลือก ให้หยุดที่ตำแหน่งเดิม
        return self.pos

    def take_damage(self, amount):
        """ลดพลังชีวิตของผี"""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """ทำให้ผีตาย"""
        self.kill()

    def reset(self, x, y):
        """รีเซ็ตตำแหน่งของผี"""
        self.pos = vec(x, y) * TILESIZE  # ตำแหน่งเริ่มต้น
        self.rect.topleft = self.pos
        self.target = self.pos  # เป้าหมายกลับไปที่จุดเริ่มต้น

class Blinky(Ghost):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, blinky_img, "red", speed=80)

class Pinky(Ghost):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, pinky_img, "pink", speed=75)

class Inky(Ghost):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, inky_img, "blue", speed=70)

class Clyde(Ghost):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, clyde_img, "orange", speed=65)