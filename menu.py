# menu.py make by Tin

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
pg.mixer.music.set_volume(0.1)
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

def difficulty_menu():
    """เมนูเลือกระดับความยาก"""
    while True:
        SCREEN.blit(BG, (0, 0))
        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()

        # แสดงข้อความหัวข้อ "Select Difficulty"
        DIFFICULTY_TEXT = get_font(80).render("SELECT DIFFICULTY", True, "#FF9966")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(820, 200))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        # สร้างปุ่ม
        EASY_BUTTON = Button(
            pos=(820, 400),
            text_input="EASY",
            font=get_font(50),
            base_color="#FF9966",
            hovering_color="White"
        )
        MEDIUM_BUTTON = Button(
            pos=(820, 500),
            text_input="MEDIUM",
            font=get_font(50),
            base_color="#FF9966",
            hovering_color="White"
        )
        HARD_BUTTON = Button(
            pos=(820, 600),
            text_input="HARD",
            font=get_font(50),
            base_color="#FF9966",
            hovering_color="White"
        )
        BACK_BUTTON = Button(
            pos=(820, 700),
            text_input="BACK",
            font=get_font(50),
            base_color="#FF9966",
            hovering_color="White"
        )

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(DIFFICULTY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    start_game("map1.txt")  # รอจน `start_game` เสร็จสิ้น
                if MEDIUM_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    start_game("map2.txt")  # รอจน `start_game` เสร็จสิ้น
                if HARD_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    start_game("map3.txt")  # รอจน `start_game` เสร็จสิ้น
                if BACK_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    """เมนูหลักที่มีปุ่ม Start และ Exit"""
    while True:
        # แสดงพื้นหลังและตำแหน่งเมาส์
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # แสดงข้อความหัวข้อเกม
        MENU_TEXT = get_font(130).render("CIRCLE-MAN", True, "#FF9966")
        MENU_RECT = MENU_TEXT.get_rect(center=(820, 300))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # สร้างปุ่ม Start และ Exit
        START_BUTTON = Button(
            pos=(820, 500),
            text_input="START",
            font=get_font(50),
            base_color="#FF9966",
            hovering_color="White"
        )
        EXIT_BUTTON = Button(
            pos=(820, 650),
            text_input="EXIT",
            font=get_font(50),
            base_color="#FF9966",
            hovering_color="White"
)

        # อัปเดตปุ่มและตรวจสอบสถานะเมาส์
        for button in [START_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # จัดการเหตุการณ์ในหน้าจอเมนูหลัก
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):  # คลิกปุ่ม Start
                    difficulty_menu()  # เปลี่ยนไปที่เมนูเลือกระดับความยาก
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):  # คลิกปุ่ม Exit
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# เริ่มต้นเกมที่เมนูหลัก
main_menu()