import pygame as pg # pg ย่อมาจาก pygame
import sys
from os import path
# import file
from sprites import *
from settings import *
from tilemap import *

# ------------------------------------ สร้าง class Game ขึ้น ------------------------------------
class Game:
    # ------------------------------- default constructor -------------------------------
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

    # -----------------------------------------------------------------------------------
    def show_start_screen(self):
        pass

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, "map1.txt"))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

    def show_go_screen(self):
        pass

    # Exit
    def quit(self):
        pg.quit()
        sys.exit()

# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

    # method วาดตารางกริด
    # def draw_grid(self):
    #     for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.scr_display, LIGHTGREY, (x,0), (x, HEIGHT))
    #     for y in range(0, HEIGHT, TILESIZE):
    #         pg.draw.line(self.scr_display, LIGHTGREY, (0,y), (WIDTH, y))

    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.scr_display.blit(text_surface, text_rect)

    def draw(self):
        self.scr_display.fill("DARKGREY")
        for sprite in self.all_sprites:
            self.scr_display.blit(sprite.image, self.camera.apply(sprite))

        # แสดงคะแนนที่มุมบนซ้ายของหน้าจอ
        self.draw_text(f"Score: {self.score}", 30, WHITE, 10, 10)

        pg.display.flip()

    # iya
    def respawn_special_fruit(self):
        # ลบผลไม้พิเศษที่มีอยู่ก่อน (ถ้ามี)
        for fruit in self.fruits:
            if isinstance(fruit, SpecialFruit):
                fruit.kill()

        # เลือกผลไม้ปกติแบบสุ่ม
        regular_fruits = [fruit for fruit in self.fruits if not isinstance(fruit, SpecialFruit)]
        if regular_fruits:
            chosen_fruit = random.choice(regular_fruits)
            chosen_fruit.kill()  # ลบผลไม้ปกติที่ถูกเลือก
            # สร้างผลไม้พิเศษใหม่ที่ตำแหน่งของผลไม้ปกติที่ถูกลบ
            SpecialFruit(self, chosen_fruit.rect.x // TILESIZE, chosen_fruit.rect.y // TILESIZE)
        else:
            print("No regular fruits available to replace.")


    # method อัพเดทตำแหน่งของสไปร์ท
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        # ตรวจจับการชนระหว่างผู้เล่นและผลไม้
        hits = pg.sprite.spritecollide(self.player, self.fruits, True)  # True เพื่อลบผลไม้ที่ชนแล้ว
        for hit in hits:
            self.update_score(1)  # เพิ่มคะแนน 10 เมื่อชนกับผลไม้
            if isinstance(hit, SpecialFruit):
                # หากเก็บผลไม้พิเศษ
                self.player.speed_boost = True  # เปิดการวิ่งเร็ว
                self.player.boost_timer = 0  # รีเซ็ตเวลา
                print("Speed Boost Activated!")
                self.respawn_special_fruit()  # เรียกฟังก์ชันสร้างผลไม้พิเศษใหม่

    def update_score(self, points):
        self.score += points

    # method อีเวนท์ต่างๆ
    def events(self):
        # กดกาที่แถบด้านบนของหน้าต่างเพื่อออกเกม
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit() # เรียกใช้งาน method ออกเกม
            # เมื่อกดปุ่มอะไรบางอย่างจะเริ่มทำงาน
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:    # กด Esc เพื่อออกเกม
                    self.quit()                 # เรียกใช้งาน method ออกเกม

    # --------------------- สร้าง method run สำหรับรันเกม  ---------------------
    def run(self):
        
        # ตราบใดที่ self.playing = True เกมก็จะยังทำงาน
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()
    # ----------------------------------------------------------------------

    def new(self):
        # สร้างกลุ่มของสไปร์ททั้งหมด
        self.all_sprites = pg.sprite.Group()
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

        # เริ่มต้นด้วยผลไม้พิเศษเพียงลูกเดียว
        self.respawn_special_fruit()

        # TimedObstacle
        TimedObstacle(self, 5, 5, appear_time=3000, disappear_time=2000)

        self.camera = Camera(self.map.width, self.map.height)

# -----------------------------------------------------

# ------------------ ส่วนของการรันเกม ------------------
# เช็คว่าชื่อโมดูลปัจจุบัน (__name__) มีค่าเป็น '__main__' หรือไม่
# ถ้าใช่ แสดงว่าไฟล์นี้ถูกเรียกใช้โดยตรง

def start_game():
    game = Game()   # สร้าง object game จาก class Game
    game.new()
    game.run()
    

# ----------------------------------------------------