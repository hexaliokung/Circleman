# menu.py make by Tin

# นำเข้าโมดูล pygame และ sys
import pygame
import sys
from settings import *  # นำเข้าการตั้งค่าทั้งหมดจากไฟล์ settings.py
import pygame as pg
from button import Button  # นำเข้า class Button
from main import start_game  # นำเข้า start_game function

# การตั้งค่าพื้นฐาน, สร้างหน้าจอ และกำหนดชื่อเกม
pygame.init()  # เริ่มต้น pygame
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # กำหนดหน้าจอเกมตามความกว้างและความสูง
pygame.display.set_caption("Circle man")  # ตั้งชื่อหน้าต่างเกม

# โหลดทรัพยากร (รูปภาพและเสียง)
BG = pygame.image.load("img/background3.webp")  # โหลดภาพพื้นหลัง
pg.mixer.music.load("img/1 - Adventure Begin.ogg")  # โหลดเพลงพื้นหลัง
pg.mixer.music.play(-1)  # เล่นเพลงซ้ำแบบ loop
pg.mixer.music.set_volume(0.1)  # ตั้งระดับเสียงของเพลง

# ฟังก์ชันสำหรับสร้างฟอนต์
def get_font(size):
    # สร้างฟอนต์ด้วยขนาดที่กำหนด และส่งคืน object ฟอนต์
    return pygame.font.Font("img/GAMEDAY.ttf", size)

# ฟังก์ชันสำหรับหน้าจอการเล่น
def play():
    # หน้าจอสำหรับเล่นเกม (placeholder)
    while True:
        # ตรวจสอบตำแหน่งของเมาส์
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # วนลูปเหตุการณ์ที่เกิดขึ้น
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # ถ้าผู้ใช้กดปิดหน้าต่าง
                pygame.quit()
                sys.exit()  # ออกจากโปรแกรม
            if event.type == pygame.MOUSEBUTTONDOWN:  # ถ้าผู้ใช้คลิกเมาส์
                main_menu()  # กลับไปที่เมนูหลัก

        # อัปเดตหน้าจอ
        pygame.display.update()

# ฟังก์ชันเมนูเลือกระดับความยาก
def difficulty_menu():
    """เมนูเลือกระดับความยาก"""
    while True:
        SCREEN.blit(BG, (0, 0))  # วาดพื้นหลัง
        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()  # ตำแหน่งของเมาส์

        # แสดงข้อความ "SELECT DIFFICULTY"
        DIFFICULTY_TEXT = get_font(80).render("SELECT DIFFICULTY", True, "#FF9966")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(820, 200))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        # สร้างปุ่มต่างๆ
        EASY_BUTTON = Button(pos=(820, 400), text_input="EASY", font=get_font(50),
                             base_color="#FF9966", hovering_color="White")
        MEDIUM_BUTTON = Button(pos=(820, 500), text_input="MEDIUM", font=get_font(50),
                               base_color="#FF9966", hovering_color="White")
        HARD_BUTTON = Button(pos=(820, 600), text_input="HARD", font=get_font(50),
                             base_color="#FF9966", hovering_color="White")
        BACK_BUTTON = Button(pos=(820, 700), text_input="BACK", font=get_font(50),
                             base_color="#FF9966", hovering_color="White")

        # อัปเดตปุ่ม (เปลี่ยนสีเมื่อเมาส์อยู่เหนือปุ่ม)
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(DIFFICULTY_MOUSE_POS)
            button.update(SCREEN)

        # วนลูปเหตุการณ์ในหน้าจอ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # หากผู้ใช้ปิดหน้าต่าง
                pygame.quit()
                sys.exit()  # ออกจากโปรแกรม
            if event.type == pygame.MOUSEBUTTONDOWN:  # ถ้าผู้ใช้คลิกเมาส์
                if EASY_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    start_game("map1.txt")  # เริ่มเกมในระดับง่าย
                if MEDIUM_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    start_game("map2.txt")  # เริ่มเกมในระดับปานกลาง
                if HARD_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    start_game("map3.txt")  # เริ่มเกมในระดับยาก
                if BACK_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):  
                    main_menu()  # กลับไปที่เมนูหลัก

        # อัปเดตหน้าจอ
        pygame.display.update()

# ฟังก์ชันเมนูหลัก
def main_menu():
    """เมนูหลักที่มีปุ่ม Start และ Exit"""
    while True:
        SCREEN.blit(BG, (0, 0))  # แสดงพื้นหลัง
        MENU_MOUSE_POS = pygame.mouse.get_pos()  # ตำแหน่งของเมาส์

        # แสดงข้อความ "CIRCLE-MAN"
        MENU_TEXT = get_font(130).render("CIRCLE-MAN", True, "#FF9966")
        MENU_RECT = MENU_TEXT.get_rect(center=(820, 300))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # สร้างปุ่ม Start และ Exit
        START_BUTTON = Button(pos=(820, 500), text_input="START", font=get_font(50),
                              base_color="#FF9966", hovering_color="White")
        EXIT_BUTTON = Button(pos=(820, 650), text_input="EXIT", font=get_font(50),
                             base_color="#FF9966", hovering_color="White")

        # อัปเดตปุ่ม (เปลี่ยนสีเมื่อเมาส์อยู่เหนือปุ่ม)
        for button in [START_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # วนลูปเหตุการณ์ในหน้าจอ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # หากผู้ใช้ปิดหน้าต่าง
                pygame.quit()
                sys.exit()  # ออกจากโปรแกรม
            if event.type == pygame.MOUSEBUTTONDOWN:  # หากผู้ใช้คลิกเมาส์
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):  
                    difficulty_menu()  # ไปที่เมนูเลือกระดับความยาก
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):  
                    pygame.quit()
                    sys.exit()  # ออกจากโปรแกรม

        # อัปเดตหน้าจอ
        pygame.display.update()

# เริ่มต้นเกมโดยเริ่มจากเมนูหลัก
main_menu()