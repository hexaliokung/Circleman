import pygame
import sys
from settings import *
import pygame as pg
from button import Button
from main import start_game

# การตั้งค่าพื้นฐาน, หน้าจอ, ชื่อเกม
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle man")

# โหลดทรัพยากร (รูปภาพและเสียง)
BG = pygame.image.load("img/background3.webp")  # ภาพพื้นหลัง
pg.mixer.music.load("img/1 - Adventure Begin.ogg")  # เพลงพื้นหลัง
pg.mixer.music.play(-1) # เพลงเล่นซ้ำเป็น loop

# ฟังก์ชันสำหรับสร้างฟอนต์
def get_font(size):
    # ส่งคืนฟอนต์ในขนาดที่ต้องการ
    return pygame.font.Font("img/GAMEDAY.ttf", size)

# ฟังก์ชันสำหรับหน้าจอการเล่น
def play():
    # ตรวจสอบตำแหน่งเมาส์และจัดการเหตุการณ์ในหน้าจอการเล่น
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()

# ฟังก์ชันสำหรับหน้าจอเมนูหลัก
def main_menu():
    """สร้างหน้าจอเมนูหลัก พร้อมปุ่ม Play และ Quit"""
    while True:
        # แสดงพื้นหลังและตำแหน่งเมาส์
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # แสดงข้อความหัวข้อเกม
        MENU_TEXT = get_font(130).render("CIRCLE-MAN", True, "#FF9966")
        MENU_RECT = MENU_TEXT.get_rect(center=(820, 300))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # สร้างปุ่ม Play และ Quit
        PLAY_BUTTON = Button(
            image=pygame.image.load("img/menu_inv_button.png"), 
            pos=(820, 500), 
            text_input="PLAY", 
            font=get_font(50), 
            base_color="#FF9966", 
            hovering_color="White"
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("img/menu_inv_button.png"), 
            pos=(820, 650), 
            text_input="QUIT", 
            font=get_font(50), 
            base_color="#FF9966", 
            hovering_color="White"
        )

        # อัปเดตปุ่มและตรวจสอบสถานะเมาส์
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # จัดการเหตุการณ์ในหน้าจอเมนู
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):  # คลิกปุ่ม Play
                    start_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):  # คลิกปุ่ม Quit
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# เริ่มต้นเกมที่เมนูหลัก
main_menu()