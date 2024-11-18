import pygame as pg
import sys
from os import path

# import file
from sprites import *
from settings import *
from tilemap import *

# Tle
class Game:
    def __init__(self, map_file):
        pg.init()

        self.scr_display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Circle man")
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)

        self.score = 0
        self.ghost_speed_effect_active = False
        self.ghost_speed_effect_timer = 0
        self.ghost_original_speed = {}
        self.map_file = map_file
        self.load_data()

    # Tle
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        sound_folder = path.join(game_folder, "sound")
        
        self.map = Map(path.join(game_folder, self.map_file))
        self.player_img = pg.image.load(path.join(img_folder, "player.png")).convert_alpha()

        self.fruit_eat_sound = pg.mixer.Sound(path.join(sound_folder, "gold3.wav"))
        self.boom = pg.mixer.Sound(path.join(sound_folder, "explosion.wav"))
        self.win_sound = pg.mixer.Sound(path.join(sound_folder, "win.wav"))
        self.lose_sound = pg.mixer.Sound(path.join(sound_folder, "lose.wav"))

    # Tle
    def quit(self):
        pg.quit()
        sys.exit()

    # Tle
    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.scr_display.blit(text_surface, text_rect)

    # Tle
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    # Tle
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    # Tle and Iya
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.fruits = pg.sprite.Group()
        self.traps = pg.sprite.Group()

        self.fruit_positions = []

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                elif tile == "P":
                    self.player = Player(self, col, row)
                elif tile == "2":
                    self.fruit_positions.append((col, row))
                elif tile == "3":
                    random_start_time = random.randint(0, 5000)
                    TimedObstacle(self, col, row, appear_time=3000, disappear_time=3500, start_time=random_start_time)
                elif tile == "4":
                    TimedTrap(self, col, row, appear_time=5000, disappear_time=3500)

                elif tile == "B":
                    ghost = Blinky(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)
                elif tile == "W":
                    ghost = Pinky(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)
                elif tile == "I":
                    ghost = Inky(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)
                elif tile == "C":
                    ghost = Clyde(self, col, row)
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)

        self.spawn_fruits()
        self.respawn_special_fruit()

        self.camera = Camera(self.map.width, self.map.height)

    # Tle and Iya
    def update(self):
        if self.ghost_speed_effect_active:
            current_time = pg.time.get_ticks()
            if current_time - self.ghost_speed_effect_timer > self.ghost_speed_effect_duration:
                self.reset_ghost_speed()

        self.all_sprites.update()
        self.camera.update(self.player)
        self.ghosts.update()
        self.traps.update()

        # Iya ตรวจจับการชนระหว่างผู้เล่นและผลไม้
        hits = pg.sprite.spritecollide(self.player, self.fruits, True)
        for hit in hits:
            self.update_score(1)
            self.fruit_eat_sound.play()

            if isinstance(hit, SpecialFruit):
                hit.apply_effect(self)
                print(f"Special effect activated: {hit.effect_type}")
                self.respawn_special_fruit()

        if not self.player.alive:
            self.game_over("GAME OVER")
            self.playing = False
        elif not self.fruits:
            self.game_over("YOU WIN!")
            self.playing = False

        # Tin ตรวจจับการชนระหว่างผู้เล่นและผี
        ghost_hits = pg.sprite.spritecollide(self.player, self.ghosts, False)
        if ghost_hits and self.player.alive:
            self.player.take_damage()
            print(f"Player hit by ghost! Lives remaining: {self.player.lives}")
            self.boom.play()

            if self.player.lives > 0:
                self.reset_positions()

        # Tle
        trap_hits = pg.sprite.spritecollide(self.player, self.traps, False)
        for trap in trap_hits:
            trap.on_player_collide(self.player)
            print("Player hit a trap! Lives remaining:", self.player.lives)

    # Tle and Iya and Tin
    def draw(self):
        self.scr_display.fill("DARKGREY")

        for sprite in self.all_sprites:
            self.scr_display.blit(sprite.image, self.camera.apply(sprite))

        self.draw_text(f"Score: {self.score}", 30, WHITE, WIDTH - 150, 10)  # เลื่อน x ไปที่ WIDTH - 150

        # Tin วาดหัวใจ
        self.draw_hearts()

        pg.display.flip()

    # Tin
    def draw_hearts(self):
        heart_image = pg.image.load('img/heart.png').convert_alpha()
        heart_image = pg.transform.scale(heart_image, (30, 30))

        for i in range(self.player.lives):
            self.scr_display.blit(heart_image, (10 + i * 40, 10))

    # Tin
    def player_died(self):
        if self.player.lives > 0:
            self.player.respawn(15, 26)

    # Iya
    def spawn_fruits(self):
        for position in self.fruit_positions:
            if random.random() < 0.6:
                Fruit(self, position[0], position[1])

    # Iya
    def respawn_special_fruit(self):
        regular_fruits = [fruit for fruit in self.fruits if not isinstance(fruit, SpecialFruit)]
        if regular_fruits:
            chosen_fruit = random.choice(regular_fruits)
            chosen_fruit.kill()

            SpecialFruit(self, chosen_fruit.rect.x // TILESIZE, chosen_fruit.rect.y // TILESIZE)

    # Iya
    def update_score(self, points):
        self.score += points

    # Tle and Iya
    def game_over(self, message):
        self.scr_display.fill(BLACK)
        self.draw_text(message, 60, WHITE, WIDTH // 2 - 150, HEIGHT // 2 - 30)

        # เลือกเสียงตามสถานะเกม
        if message == "YOU WIN!":
            self.win_sound.play()   # เล่นเสียงชนะ
        elif message == "GAME OVER":
            self.lose_sound.play()  # เล่นเสียงแพ้

        # แสดงข้อความคำแนะนำเพิ่มเติม
        self.draw_text("Press R to Restart, Q to Quit, or B to Menu",\
                        30, WHITE, WIDTH // 2 - 200, HEIGHT // 2 + 50)
        pg.display.flip()

        # รอการตอบสนองของผู้เล่น
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:       # หากปิดหน้าต่าง ออกจากเกม
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:     # กด R เพื่อเริ่มเกมใหม่
                        waiting = False
                        self.new()
                        self.run()
                    elif event.key == pg.K_q:   # กด Q เพื่อออกจากเกม
                        self.quit()
                    elif event.key == pg.K_b:   # เพิ่มปุ่มกลับไปที่เมนูเลือกโหมด
                        waiting = False
                        return

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
        self.player.respawn(26, 15)  # กำหนดตำแหน่งเริ่มต้นของผู้เล่น (เปลี่ยนได้ตามแผนที่)

        # รีเซ็ตตำแหน่งของผี
        for ghost in self.ghosts:
            if isinstance(ghost, Blinky):  # สำหรับผีแต่ละชนิด
                ghost.pos = vec(1, 1) * TILESIZE  # กำหนดตำแหน่งเริ่มต้นของ Blinky
            elif isinstance(ghost, Pinky):
                ghost.pos = vec(51, 1) * TILESIZE  # ตำแหน่งเริ่มต้นของ Pinky
            elif isinstance(ghost, Inky):
                ghost.pos = vec(1, 31) * TILESIZE  # ตำแหน่งเริ่มต้นของ Inky
            elif isinstance(ghost, Clyde):
                ghost.pos = vec(51, 31) * TILESIZE  # ตำแหน่งเริ่มต้นของ Clyde

            ghost.target = ghost.pos  # ตั้งเป้าหมายเป็นตำแหน่งเริ่มต้น
            ghost.rect.topleft = ghost.pos  # อัปเดตตำแหน่ง sprite

    def modify_ghost_speed(self, multiplier):
        for ghost in self.ghosts:
            ghost.speed *= multiplier
            ghost.speed = max(30, min(100, ghost.speed))  # จำกัดความเร็วให้อยู่ระหว่าง 30 ถึง 100

    def apply_ghost_speed_effect(self, multiplier, duration):
        """เริ่มต้นผลกระทบเพิ่ม/ลดความเร็วของผี"""
        if not self.ghost_speed_effect_active:
            # เก็บความเร็วเริ่มต้นของผีทุกตัว
            for ghost in self.ghosts:
                self.ghost_original_speed[ghost] = ghost.speed

            # ปรับความเร็วของผีทั้งหมด
            self.modify_ghost_speed(multiplier)

            # ตั้งค่าตัวจับเวลา
            self.ghost_speed_effect_active = True
            self.ghost_speed_effect_timer = pg.time.get_ticks()  # เวลาเริ่มต้นในมิลลิวินาที

        # ระยะเวลาของเอฟเฟกต์
        self.ghost_speed_effect_duration = duration

    def reset_ghost_speed(self):
        """รีเซ็ตความเร็วของผีทั้งหมดกลับไปเป็นค่าปกติ"""
        for ghost in self.ghosts:
            if ghost in self.ghost_original_speed:
                ghost.speed = self.ghost_original_speed[ghost]  # คืนค่าความเร็วเดิม

        # ล้างสถานะเอฟเฟกต์
        self.ghost_speed_effect_active = False
        self.ghost_original_speed.clear()

# Tin
def start_game(map_file):
    if not pg.mixer.music.get_busy():
        pg.mixer.music.load("img/game_music.ogg")
        pg.mixer.music.play(-1)

    game = Game(map_file)
    game.new()
    game.run()