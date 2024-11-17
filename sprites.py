import pygame as pg
import random
import heapq

from settings import *
vec = pg.math.Vector2

# Tle and Iya and Tin
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)  # เรียกใช้ constructor ของ Sprite โดยตรง
        self.game = game
        self.image = pg.Surface(((TILESIZE // 4) * 3, (TILESIZE // 4) * 3))
        self.image = pg.image.load("img/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.speed_boost = False
        self.boost_timer = 0
        self.boost_time = 5000  # Default boost time of 5 seconds

        # Tin จำนวนชีวิตเริ่มต้น
        self.lives = 3
        # Tin กำหนดสถานะว่ายังมีชีวิต
        self.alive = True

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

    # Tin
    def take_damage(self):
        """ลดจำนวนชีวิตลงเมื่อโดนศัตรูหรืออุปสรรค"""
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.alive = False  # ตัวละครตาย
            self.game.player_died()  # เรียกฟังก์ชันในเกมเมื่อผู้เล่นตาย

    # Tin
    def respawn(self, x, y):
        self.alive = True
        self.pos = vec(x, y) * TILESIZE  # ตำแหน่งเริ่มต้น
        self.rect.topleft = self.pos
        self.vel = vec(0, 0)  # รีเซ็ตความเร็ว

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
    def __init__(self, game, x, y, appear_time=2000, disappear_time=2000, start_time=0):
        # เพิ่มวัตถุอุปสรรคเข้าสู่กลุ่ม sprites และ obstacles
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)  # กำหนดสีพื้นหลังของ obstacle เป็นสีดำ
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
        self.appear_time = appear_time  # ระยะเวลาที่ obstacle จะปรากฏ
        self.disappear_time = disappear_time  # ระยะเวลาที่ obstacle จะหายไป
        self.start_time = start_time  # เวลาที่ obstacle จะเริ่มทำงาน
        self.timer = -self.start_time  # ตั้งค่าเริ่มต้น (ลบ start_time เพื่อรอให้ถึงเวลาเริ่ม)
        self.visible = False  # กำหนดให้ obstacle เริ่มต้นด้วยสถานะไม่แสดงผล

    def update(self):
        # เพิ่มค่าของ timer โดยแปลง delta time เป็นหน่วยมิลลิวินาที
        self.timer += self.game.dt * 1000  

        # ตรวจสอบว่า timer ถึงเวลาที่ obstacle ควรเริ่มทำงานหรือยัง
        if self.timer >= 0:  
            # ตรวจสอบสถานะ visible และจัดการการปรากฏ/หายของ obstacle
            if self.visible and self.timer >= self.appear_time:
                self.visible = False  # ตั้งค่าให้ obstacle หายไป
                self.image.set_alpha(0)  # ตั้งค่าความโปร่งใส (ทำให้มองไม่เห็น)
                self.timer = 0
                # ลบ obstacle ออกจากกลุ่ม obstacles เพื่อไม่ให้ชนกับผู้เล่น
                self.game.obstacles.remove(self)
            elif not self.visible and self.timer >= self.disappear_time:
                self.visible = True  # ตั้งค่าให้ obstacle ปรากฏ
                self.image.set_alpha(255)  # ตั้งค่าความโปร่งใส (ทำให้มองเห็นได้)
                self.image.fill(BLACK)  # เติมสีดำให้ obstacle
                self.timer = 0
                # เพิ่ม obstacle กลับเข้าสู่กลุ่ม obstacles เพื่อชนกับผู้เล่น
                self.game.obstacles.add(self)

# Tle
# คลาสสำหรับกับดักที่เปิด-ปิดได้ตามเวลา
class TimedTrap(pg.sprite.Sprite):
    def __init__(self, game, x, y, appear_time=5000, disappear_time=3500):
        self.groups = game.all_sprites, game.traps  # เพิ่มไปยังกลุ่ม traps
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)  # สีแดงแสดงถึงกับดัก
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.appear_time = appear_time
        self.disappear_time = disappear_time
        self.timer = 0
        self.visible = True

    def update(self):
        # อัปเดตเวลาเปิด-ปิดของกับดัก
        self.timer += self.game.dt * 1000  # คำนวณเวลาเป็นมิลลิวินาที

        if self.visible and self.timer >= self.appear_time:
            self.visible = False
            self.image.set_alpha(0)  # ซ่อนกับดัก (โปร่งใส)
            self.timer = 0
        elif not self.visible and self.timer >= self.disappear_time:
            self.visible = True
            self.image.set_alpha(255)  # แสดงกับดัก
            self.timer = 0

    def on_player_collide(self, player):
        """ลดหัวใจของผู้เล่นลง 1 และรีเซ็ตตำแหน่งเมื่อชนกับดัก"""
        if self.visible:  # ตรวจสอบว่ากับดักเปิดอยู่หรือไม่
            player.take_damage()
            if player.lives > 0:  # ถ้าผู้เล่นยังมีชีวิต รีเซ็ตตำแหน่ง
                self.game.reset_positions()
            else:  # ถ้าผู้เล่นไม่มีชีวิต เกมจะจบ
                print("Game Over")

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
        super().__init__(game, x, y)

        self.image.fill((0, 0, 0, 0))  # ล้างพื้นหลังให้โปร่งใส
        pg.draw.circle(self.image, RED, (TILESIZE // 2, TILESIZE // 2), TILESIZE // 3)

        # เพิ่มความสามารถแบบสุ่ม
        self.effect_type = random.choice(["speed_up", "speed_down", "ghost_speed_up", "ghost_speed_down"])
        self.boost_time = 5000  # ระยะเวลาผลของเอฟเฟกต์ 5 วินาที

    def apply_effect(self, game):
        if self.effect_type == "speed_up":
            game.player.speed_boost = True
            game.player.boost_timer = 0
            game.player.speed_multiplier = 1.2  # เพิ่มความเร็วผู้เล่น
        elif self.effect_type == "speed_down":
            game.player.speed_boost = True
            game.player.boost_timer = 0
            game.player.speed_multiplier = 0.9  # ลดความเร็วผู้เล่น
        elif self.effect_type == "ghost_speed_up":
            game.apply_ghost_speed_effect(multiplier=1.5, duration=5000)  # เพิ่มความเร็วผี 5 วินาที
        elif self.effect_type == "ghost_speed_down":
            game.apply_ghost_speed_effect(multiplier=0.5, duration=5000)  # ลดความเร็วผี 5 วินาที

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

    def reset(self, x, y):
        """รีเซ็ตตำแหน่งของผี"""
        self.pos = vec(x, y) * TILESIZE  # ตำแหน่งเริ่มต้น
        self.rect.topleft = self.pos
        self.target = self.pos  # เป้าหมายกลับไปที่จุดเริ่มต้น

# Pao
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