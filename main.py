import pygame as pg
import sys
from os import path

# import file
from sprites import *  # นำเข้าไฟล์ที่เกี่ยวข้องกับ sprite ทั้งหมด
from settings import *  # นำเข้าการตั้งค่าทั้งหมด
from tilemap import *  # นำเข้าการจัดการแผนที่

# Tle
class Game:
    def __init__(self, map_file):
        pg.init()  # เริ่มต้น pygame

        # สร้างหน้าจอเกม
        self.scr_display = pg.display.set_mode((WIDTH, HEIGHT))  # ตั้งค่าหน้าจอด้วยความกว้างและสูง
        pg.display.set_caption("Circle man")  # ตั้งชื่อหน้าต่างเกม
        self.clock = pg.time.Clock()  # ตัวจับเวลาสำหรับควบคุม FPS
        pg.key.set_repeat(100, 100)  # ตั้งค่าการตรวจจับการกดปุ่มซ้ำ

        self.score = 0  # ตัวแปรสำหรับเก็บคะแนนของผู้เล่น
        self.ghost_speed_effect_active = False  # ตรวจสอบว่าเอฟเฟกต์ผีเปิดใช้งานหรือไม่
        self.ghost_speed_effect_timer = 0  # ตัวจับเวลาเอฟเฟกต์ผี
        self.ghost_original_speed = {}  # เก็บความเร็วดั้งเดิมของผี
        self.map_file = map_file  # ชื่อไฟล์แผนที่
        self.load_data()  # โหลดข้อมูลที่จำเป็น

    # Tle
    def load_data(self):
        """โหลดข้อมูลแผนที่ รูปภาพ และเสียง"""
        game_folder = path.dirname(__file__)  # โฟลเดอร์หลักของไฟล์เกม
        img_folder = path.join(game_folder, "img")  # โฟลเดอร์รูปภาพ
        sound_folder = path.join(game_folder, "sound")  # โฟลเดอร์เสียง
        
        self.map = Map(path.join(game_folder, self.map_file))  # โหลดข้อมูลแผนที่จากไฟล์
        self.player_img = pg.image.load(path.join(img_folder, "player.png")).convert_alpha()  # โหลดภาพตัวผู้เล่น

        # โหลดเสียงต่างๆ
        self.fruit_eat_sound = pg.mixer.Sound(path.join(sound_folder, "gold3.wav"))  # เสียงเก็บผลไม้
        self.boom = pg.mixer.Sound(path.join(sound_folder, "explosion.wav"))  # เสียงระเบิดเมื่อชน
        self.win_sound = pg.mixer.Sound(path.join(sound_folder, "win.wav"))  # เสียงเมื่อชนะ
        self.lose_sound = pg.mixer.Sound(path.join(sound_folder, "lose.wav"))  # เสียงเมื่อแพ้

    # Tle
    def quit(self):
        """ออกจากเกม"""
        pg.quit()  # ปิด pygame
        sys.exit()  # ออกจากโปรแกรม

    # Tle
    def draw_text(self, text, size, color, x, y):
        """วาดข้อความบนหน้าจอ"""
        font = pg.font.SysFont(None, size)  # สร้างฟอนต์
        text_surface = font.render(text, True, color)  # สร้างข้อความด้วยฟอนต์
        text_rect = text_surface.get_rect()  # กำหนดกรอบของข้อความ
        text_rect.topleft = (x, y)  # ตำแหน่งของข้อความ
        self.scr_display.blit(text_surface, text_rect)  # วาดข้อความลงบนหน้าจอ

    # Tle
    def events(self):
        """จัดการเหตุการณ์ต่างๆ ในเกม"""
        for event in pg.event.get():  # ตรวจสอบเหตุการณ์ที่เกิดขึ้น
            if event.type == pg.QUIT:  # หากกดปิดหน้าต่าง
                self.quit()  # เรียกใช้งานฟังก์ชัน quit
            if event.type == pg.KEYDOWN:  # หากกดปุ่มใดๆ
                if event.key == pg.K_ESCAPE:  # หากกดปุ่ม ESC
                    self.quit()  # ออกจากเกม

    # Tle
    def run(self):
        """วนลูปการทำงานของเกม"""
        self.playing = True  # ตั้งค่าเกมให้กำลังทำงาน
        while self.playing:  # วนลูปตราบใดที่ยังเล่นเกมอยู่
            self.dt = self.clock.tick(FPS)/1000  # คำนวณเวลาที่ผ่านไปในแต่ละเฟรม
            self.events()  # ตรวจสอบเหตุการณ์
            self.update()  # อัปเดตสถานะเกม
            self.draw()  # วาดทุกอย่างบนหน้าจอ

    # Tle and Iya
    def new(self):
        """เริ่มเกมใหม่และสร้างวัตถุต่างๆ"""
        self.all_sprites = pg.sprite.Group()  # กลุ่มวัตถุทั้งหมด
        self.ghosts = pg.sprite.Group()  # กลุ่มผี
        self.walls = pg.sprite.Group()  # กลุ่มกำแพง
        self.obstacles = pg.sprite.Group()  # กลุ่มสิ่งกีดขวาง
        self.fruits = pg.sprite.Group()  # กลุ่มผลไม้
        self.traps = pg.sprite.Group()  # กลุ่มกับดัก

        self.fruit_positions = []  # เก็บตำแหน่งผลไม้

        # สร้างวัตถุตามแผนที่
        for row, tiles in enumerate(self.map.data):  # วนลูปตามแถวในแผนที่
            for col, tile in enumerate(tiles):  # วนลูปแต่ละคอลัมน์ในแถว
                if tile == "1":  # ถ้าเป็นกำแพง
                    Wall(self, col, row)  # สร้างวัตถุกำแพง
                elif tile == "P":  # ถ้าเป็นผู้เล่น
                    self.player = Player(self, col, row)  # สร้างตัวผู้เล่น
                elif tile == "2":  # ตำแหน่งผลไม้
                    self.fruit_positions.append((col, row))  # บันทึกตำแหน่งผลไม้
                elif tile == "3":  # สิ่งกีดขวางแบบตั้งเวลา
                    random_start_time = random.randint(0, 5000)  # สุ่มเวลาเริ่มต้น
                    TimedObstacle(self, col, row, appear_time=3000, disappear_time=3500, start_time=random_start_time)
                elif tile == "4":  # กับดักที่เปิด/ปิด
                    TimedTrap(self, col, row, appear_time=5000, disappear_time=3500)
                elif tile == "B":  # ผีแดง
                    ghost = Blinky(self, col, row)
                    self.ghosts.add(ghost)  # เพิ่มผีลงในกลุ่ม
                    self.all_sprites.add(ghost)
                elif tile == "W":  # ผีชมพู
                    ghost = Pinky(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)
                elif tile == "I":  # ผีฟ้า
                    ghost = Inky(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)
                elif tile == "C":  # ผีส้ม
                    ghost = Clyde(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)

        self.spawn_fruits()  # สุ่มสร้างผลไม้ธรรมดา
        self.respawn_special_fruit()  # สร้างผลไม้พิเศษ

        self.camera = Camera(self.map.width, self.map.height)  # สร้างกล้อง

    # Tle and Iya
    def update(self):
        """อัปเดตสถานะเกม"""
        # ตรวจสอบว่าเอฟเฟกต์ความเร็วของผียังเปิดอยู่หรือไม่
        if self.ghost_speed_effect_active:
            current_time = pg.time.get_ticks()
            if current_time - self.ghost_speed_effect_timer > self.ghost_speed_effect_duration:
                self.reset_ghost_speed()  # รีเซ็ตความเร็วของผี

        self.all_sprites.update()  # อัปเดตวัตถุทั้งหมด
        self.camera.update(self.player)  # อัปเดตตำแหน่งกล้อง
        self.ghosts.update()  # อัปเดตตำแหน่งของผี
        self.traps.update()  # อัปเดตสถานะกับดัก

        # ตรวจสอบการชนระหว่างผู้เล่นกับผลไม้
        hits = pg.sprite.spritecollide(self.player, self.fruits, True)
        for hit in hits:
            self.update_score(1)  # เพิ่มคะแนน
            self.fruit_eat_sound.play()  # เล่นเสียงเก็บผลไม้
            if isinstance(hit, SpecialFruit):  # ถ้าเป็นผลไม้พิเศษ
                hit.apply_effect(self)  # ใช้เอฟเฟกต์ของผลไม้พิเศษ
                print(f"Special effect activated: {hit.effect_type}")
                self.respawn_special_fruit()  # สร้างผลไม้พิเศษใหม่

        # ตรวจสอบว่าผู้เล่นยังมีชีวิตหรือไม่
        if not self.player.alive:
            self.game_over("GAME OVER")  # แสดงข้อความแพ้
            self.playing = False
        elif not self.fruits:  # ถ้าผลไม้หมด
            self.game_over("YOU WIN!")  # แสดงข้อความชนะ
            self.playing = False

        # ตรวจจับการชนระหว่างผู้เล่นและผี
        ghost_hits = pg.sprite.spritecollide(self.player, self.ghosts, False)
        if ghost_hits and self.player.alive:  # ถ้าชนกับผี
            self.player.take_damage()  # ลดชีวิตผู้เล่น
            print(f"Player hit by ghost! Lives remaining: {self.player.lives}")
            self.boom.play()  # เล่นเสียงระเบิด
            if self.player.lives > 0:
                self.reset_positions()  # รีเซ็ตตำแหน่ง

        # ตรวจจับการชนกับกับดัก
        trap_hits = pg.sprite.spritecollide(self.player, self.traps, False)
        for trap in trap_hits:
            trap.on_player_collide(self.player)  # ลดชีวิตเมื่อชนกับดัก
            print("Player hit a trap! Lives remaining:", self.player.lives)

    # Tle and Iya and Tin
    def draw(self):
        # เติมสีพื้นหลังของหน้าจอด้วยสี DARKGREY
        self.scr_display.fill("DARKGREY")

        # วาด sprite ทั้งหมดในเกม โดยปรับตำแหน่ง sprite ตามกล้อง
        for sprite in self.all_sprites:
            self.scr_display.blit(sprite.image, self.camera.apply(sprite))

        # แสดงคะแนนที่มุมขวาบนของหน้าจอ
        self.draw_text(f"Score: {self.score}", 30, WHITE, WIDTH - 150, 10)

        # เรียกใช้ฟังก์ชันวาดหัวใจ แสดงจำนวนชีวิตของผู้เล่นที่เหลืออยู่
        self.draw_hearts()

        # อัปเดตหน้าจอหลังจากวาดทั้งหมดเสร็จ
        pg.display.flip()

    # Tin
    def draw_hearts(self):
        # โหลดภาพหัวใจจากไฟล์และปรับขนาดให้เล็กลง
        heart_image = pg.image.load('img/heart.png').convert_alpha()
        heart_image = pg.transform.scale(heart_image, (30, 30))

        # วาดหัวใจตามจำนวนชีวิตที่เหลือ โดยวางตำแหน่งหัวใจเรียงจากซ้ายไปขวา
        for i in range(self.player.lives):
            self.scr_display.blit(heart_image, (10 + i * 40, 10))

    # Tin
    def player_died(self):
        # ถ้าผู้เล่นยังมีชีวิตเหลือ ให้เกิดใหม่ที่ตำแหน่งเริ่มต้น
        if self.player.lives > 0:
            self.player.respawn(15, 26)

    # Iya
    def spawn_fruits(self):
        # สุ่มตำแหน่งการเกิดผลไม้ธรรมดาจากตำแหน่งที่กำหนดไว้
        for position in self.fruit_positions:
            if random.random() < 0.6:  # โอกาส 60% ที่จะเกิดผลไม้ในตำแหน่งนั้น
                Fruit(self, position[0], position[1])

    # Iya
    def respawn_special_fruit(self):
        # ค้นหาผลไม้ธรรมดาทั้งหมดที่อยู่ในเกม
        regular_fruits = [fruit for fruit in self.fruits if not isinstance(fruit, SpecialFruit)]
        if regular_fruits:
            # เลือกผลไม้ธรรมดาแบบสุ่มแล้วลบออกจากเกม
            chosen_fruit = random.choice(regular_fruits)
            chosen_fruit.kill()

            # สร้างผลไม้พิเศษในตำแหน่งของผลไม้ที่ถูกลบ
            SpecialFruit(self, chosen_fruit.rect.x // TILESIZE, chosen_fruit.rect.y // TILESIZE)

    # Iya
    def update_score(self, points):
        # เพิ่มคะแนนของผู้เล่นตามค่า points ที่ส่งมา
        self.score += points

    # Tle and Iya
    def game_over(self, message):
        # เติมพื้นหลังเป็นสีดำ
        self.scr_display.fill(BLACK)

        # แสดงข้อความจบเกม เช่น "YOU WIN!" หรือ "GAME OVER"
        self.draw_text(message, 60, WHITE, WIDTH // 2 - 150, HEIGHT // 2 - 30)

        # เล่นเสียงตามสถานะของเกม
        if message == "YOU WIN!":
            self.win_sound.play()   # เล่นเสียงชนะ
        elif message == "GAME OVER":
            self.lose_sound.play()  # เล่นเสียงแพ้

        # แสดงข้อความคำแนะนำเพิ่มเติม เช่น ปุ่ม Restart หรือ Quit
        self.draw_text("Press R to Restart, Q to Quit, or B to Menu", \
                       30, WHITE, WIDTH // 2 - 200, HEIGHT // 2 + 50)

        # อัปเดตหน้าจอเพื่อให้ข้อความแสดงผล
        pg.display.flip()

        # รอการตอบสนองจากผู้เล่น เช่น กดปุ่มเพื่อเลือกการกระทำ
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:       # ถ้าผู้ใช้ปิดหน้าต่าง
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:     # กด R เพื่อเริ่มเกมใหม่
                        waiting = False
                        self.new()
                        self.run()
                    elif event.key == pg.K_q:   # กด Q เพื่อออกจากเกม
                        self.quit()
                    elif event.key == pg.K_b:   # กด B เพื่อกลับไปที่เมนูหลัก
                        waiting = False
                        return

    # Pao
    def is_wall(self, x, y):
        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return True
        return False

    def reset_positions(self):
        self.player.respawn(26, 15)

        for ghost in self.ghosts:
            if isinstance(ghost, Blinky):
                ghost.pos = vec(1, 1) * TILESIZE
            elif isinstance(ghost, Pinky):
                ghost.pos = vec(51, 1) * TILESIZE
            elif isinstance(ghost, Inky):
                ghost.pos = vec(1, 31) * TILESIZE
            elif isinstance(ghost, Clyde):
                ghost.pos = vec(51, 31) * TILESIZE

            ghost.target = ghost.pos
            ghost.rect.topleft = ghost.pos

    def modify_ghost_speed(self, multiplier):
        for ghost in self.ghosts:
            ghost.speed *= multiplier
            ghost.speed = max(30, min(100, ghost.speed))

    def apply_ghost_speed_effect(self, multiplier, duration):
        if not self.ghost_speed_effect_active:
            for ghost in self.ghosts:
                self.ghost_original_speed[ghost] = ghost.speed

            self.modify_ghost_speed(multiplier)

            self.ghost_speed_effect_active = True
            self.ghost_speed_effect_timer = pg.time.get_ticks()

        self.ghost_speed_effect_duration = duration

    def reset_ghost_speed(self):
        for ghost in self.ghosts:
            if ghost in self.ghost_original_speed:
                ghost.speed = self.ghost_original_speed[ghost]

        self.ghost_speed_effect_active = False
        self.ghost_original_speed.clear()

def start_game(map_file):
    if not pg.mixer.music.get_busy():
        pg.mixer.music.load("img/game_music.ogg")
        pg.mixer.music.play(-1)

    game = Game(map_file)
    game.new()
    game.run()