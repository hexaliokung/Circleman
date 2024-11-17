import pygame as pg # pg ย่อมาจาก pygame
import sys
from os import path

# import file
from sprites import *
from settings import *
from tilemap import *

# Tle
class Game:

    # Tle
    def __init__(self):

        # เริ่มต้น pygame
        pg.init()

        # หน้าต่างแสดงผลให้มีขนาด = WIDTH, HEIGHT
        self.scr_display = pg.display.set_mode((WIDTH, HEIGHT))

        # ตั้งค่าชื่อของหน้าต่างเกม ซึ่งจะแสดงที่แถบด้านบนของหน้าต่าง
        pg.display.set_caption("Circle man")

        # ใช้สำหรับควบคุมความเร็วในการอัปเดตและการแสดงผลของเกม
        self.clock = pg.time.Clock()

        # ใช้สำหรับการตั้งค่าการทำซ้ำของการกดปุ่มคีย์บอร์ด เมื่อผู้ใช้กดปุ่มค้างไว้
        # โปรแกรมจะรับรู้ว่าปุ่มถูกกดซ้ำตามช่วงเวลาที่กำหนด
        pg.key.set_repeat(100, 100) # (เวลารอตรวจจับกดปุ่มซ้ำหลังจากกดปุ่มค้างไว้, ตรวจจับว่ากดซ้ำเรื่อยๆในอีก...ตราบใดที่ยังกด)

        # ตัวแปรคะแนน
        self.score = 0

        self.load_data()

    # Tle
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, "map1.txt"))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

    # Tle
    def quit(self):
        pg.quit()
        sys.exit()

    # method วาดตารางกริด
    # def draw_grid(self):
    #     for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.scr_display, LIGHTGREY, (x,0), (x, HEIGHT))
    #     for y in range(0, HEIGHT, TILESIZE):
    #         pg.draw.line(self.scr_display, LIGHTGREY, (0,y), (WIDTH, y))

    # Tle
    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.scr_display.blit(text_surface, text_rect)

    # Tle
    def events(self):   # method อีเวนท์ต่างๆ
        # กดกาที่แถบด้านบนของหน้าต่างเพื่อออกเกม
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit() # เรียกใช้งาน method ออกเกม
            # เมื่อกดปุ่มอะไรบางอย่างจะเริ่มทำงาน
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:    # กด Esc เพื่อออกเกม
                    self.quit()                 # เรียกใช้งาน method ออกเกม

    # Tle
    def run(self):
        
        # ตราบใดที่ self.playing = True เกมก็จะยังทำงาน
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    # Tle and Iya
    def new(self):
        # สร้างกลุ่มของสไปร์ททั้งหมด
        self.all_sprites = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.fruits = pg.sprite.Group()

        # สร้างภาพตามไฟล์
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":  # กำแพง
                    Wall(self, col, row)
                elif tile == "P":  # ผู้เล่น
                    self.player = Player(self, col, row)
                elif tile == "2":  # ผลไม้ปกติ
                    Fruit(self, col, row)

                elif tile == "B":  # ผีแดง (Blinky)
                    ghost = Blinky(self, col, row)
                    self.ghosts.add(ghost)  # เพิ่ม Blinky ในกลุ่มผี
                    self.all_sprites.add(ghost)  # เพิ่ม Blinky ในกลุ่มสไปร์ททั้งหมด

                elif tile == "W":  # ผีชมพู (Pinky)
                    ghost = Pinky(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)

                elif tile == "I":  # ผีฟ้า (Inky)
                    ghost = Inky(self, col, row)
                    self.ghosts.add(ghost)  # เพิ่ม Inky ในกลุ่มผี
                    self.all_sprites.add(ghost)  # เพิ่ม Inky ในกลุ่มสไปร์ททั้งหมด

                elif tile == "C":  # ผีส้ม (Clyde)
                    ghost = Clyde(self, col, row)
                    self.ghosts.add(ghost)  # เพิ่ม Clyde ในกลุ่มผี
                    self.all_sprites.add(ghost)  # เพิ่ม Clyde ในกลุ่มสไปร์ททั้งหมด

        # เริ่มต้นด้วยผลไม้พิเศษเพียงลูกเดียว
        self.respawn_special_fruit()

        # เรียกใช้ TimedObstacle
        TimedObstacle(self, 5, 5, appear_time=3000, disappear_time=2000)

        self.camera = Camera(self.map.width, self.map.height)

    # Tle and Iya
    def update(self):   # method อัพเดทตำแหน่งของสไปร์ท
        self.all_sprites.update()
        self.camera.update(self.player)
        self.ghosts.update()  # อัปเดตตำแหน่งของผี

        # Iya ตรวจจับการชนระหว่างผู้เล่นและผลไม้
        hits = pg.sprite.spritecollide(self.player, self.fruits, True)  # True เพื่อลบผลไม้ที่ชนแล้ว
        for hit in hits:
            self.update_score(1)    # เพิ่มคะแนน 1 เมื่อชนกับผลไม้

            # ใน update function ของ Game class
            if isinstance(hit, SpecialFruit):

                # ใช้เอฟเฟกต์ผลไม้พิเศษกับผู้เล่น
                hit.apply_effect(self.player)
                print(f"Special effect activated: {hit.effect_type}")

                # สร้างผลไม้พิเศษใหม่
                self.respawn_special_fruit()

        # Tin ตรวจจับการชนระหว่างผู้เล่นและผี
        ghost_hits = pg.sprite.spritecollide(self.player, self.ghosts, False)  # False ไม่ลบผี
        if ghost_hits and self.player.alive:
            self.player.take_damage()  # ลดจำนวนชีวิตของผู้เล่น
            print(f"Player hit by ghost! Lives remaining: {self.player.lives}")

            # ถ้าผู้เล่นยังมีชีวิตเหลือ รีเซ็ตตำแหน่ง
            if self.player.lives > 0:
                self.reset_positions()

    # Tle and Iya and Tin
    def draw(self):
        self.scr_display.fill("DARKGREY")
        for sprite in self.all_sprites:
            self.scr_display.blit(sprite.image, self.camera.apply(sprite))

        # Iya แสดงคะแนนที่มุมบนขวาของหน้าจอ
        self.draw_text(f"Score: {self.score}", 30, WHITE, WIDTH - 150, 10)  # เลื่อน x ไปที่ WIDTH - 150

        # Tin วาดหัวใจ
        self.draw_hearts()
        pg.display.flip()

    # Tin
    def draw_hearts(self):
        """แสดงหัวใจที่มุมซ้ายบนตามจำนวนชีวิตที่เหลือของผู้เล่น"""
        heart_image = pg.image.load('img/heart.png').convert_alpha()  # โหลดรูปภาพหัวใจ
        heart_image = pg.transform.scale(heart_image, (30, 30))  # ปรับขนาดหัวใจให้เล็กลง

        for i in range(self.player.lives):
            self.scr_display.blit(heart_image, (10 + i * 40, 10))  # วาดหัวใจโดยเว้นระยะห่าง 40 พิกเซล

    # Tin
    def player_died(self):
        """จัดการเมื่อผู้เล่นตาย"""
        if self.player.lives > 0:
            # ถ้ายังมีชีวิตเหลือ ให้เกิดใหม่ที่ตำแหน่งเริ่มต้น
            self.player.respawn(5, 5)  # ตำแหน่งเริ่มต้น
        else:
            print("Game Over")  # แสดงข้อความเมื่อเกมจบ
            self.playing = False  # จบเกม

    # Iya
    def respawn_special_fruit(self):

        # เลือกผลไม้ปกติแบบสุ่ม
        regular_fruits = [fruit for fruit in self.fruits if not isinstance(fruit, SpecialFruit)]
        if regular_fruits:
            chosen_fruit = random.choice(regular_fruits)
            chosen_fruit.kill()  # ลบผลไม้ปกติที่ถูกเลือก

            # สร้างผลไม้พิเศษในตำแหน่งที่ถูกลบ
            SpecialFruit(self, chosen_fruit.rect.x // TILESIZE, chosen_fruit.rect.y // TILESIZE)
        else:
            # ระบบทดสอบว่าถ้าผลไม้ปกติหมดผลไม้พิเศษจะไม่เกิดอีก
            print("No regular fruits available to replace.")

    # Iya
    def update_score(self, points):
        self.score += points

    # Pao
    def is_wall(self, x, y):
        """ตรวจสอบว่าตำแหน่ง (x, y) เป็นกำแพงหรือไม่"""
        # ตรวจสอบว่าในตำแหน่ง (x, y) มีวัตถุ Wall หรือไม่
        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return True
        return False

    def reset_positions(self):  # reset ตำแหน่งผู้เล่นและผีเริ่มต้น
        # รีเซ็ตตำแหน่งผู้เล่น
        self.player.respawn(32, 20)  # กำหนดตำแหน่งเริ่มต้นของผู้เล่น (เปลี่ยนได้ตามแผนที่)

        # รีเซ็ตตำแหน่งของผี
        for ghost in self.ghosts:
            if isinstance(ghost, Blinky):  # สำหรับผีแต่ละชนิด
                ghost.pos = vec(7, 7) * TILESIZE  # กำหนดตำแหน่งเริ่มต้นของ Blinky
            elif isinstance(ghost, Pinky):
                ghost.pos = vec(10, 10) * TILESIZE  # ตำแหน่งเริ่มต้นของ Pinky
            elif isinstance(ghost, Inky):
                ghost.pos = vec(12, 7) * TILESIZE  # ตำแหน่งเริ่มต้นของ Inky
            elif isinstance(ghost, Clyde):
                ghost.pos = vec(7, 12) * TILESIZE  # ตำแหน่งเริ่มต้นของ Clyde

            ghost.target = ghost.pos  # ตั้งเป้าหมายเป็นตำแหน่งเริ่มต้น
            ghost.rect.topleft = ghost.pos  # อัปเดตตำแหน่ง sprite

    def modify_ghost_speed(self, multiplier):
        """ปรับความเร็วของผีทั้งหมด"""
        for ghost in self.ghosts:
            ghost.speed *= multiplier  # ปรับความเร็วตาม multiplier
            ghost.speed = max(50, min(300, ghost.speed))  # จำกัดความเร็วให้อยู่ในช่วงที่เหมาะสม

# Tin
def start_game():
    # ตั้งค่าเพลงใหม่ในเกม (เฉพาะเมื่อเปลี่ยนเพลง)
    if not pg.mixer.music.get_busy():  # ตรวจสอบว่าเพลงกำลังเล่นอยู่หรือไม่
        pg.mixer.music.load("img/game_music.ogg")  # เปลี่ยนเพลงสำหรับเกม
        pg.mixer.music.play(-1)  # เล่นเพลงแบบวนลูป

    game = Game()
    game.new()
    game.run()