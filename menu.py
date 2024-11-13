import pygame, sys
import pygame as pg
from button import Button
from main import start_game
pygame.init()

SCREEN = pygame.display.set_mode((1600, 960))
pygame.display.set_caption("Menu")

BG = pygame.image.load("img/background3.webp")  # เพิ่มรูปภาพ
pg.mixer.music.load("img/1 - Adventure Begin.ogg")  # เพิ่มเสียง
pg.mixer.music.play(-1)

def get_font(size): #ส่งคืนฟอนด์ในขนาดที่ต้องการ
    return pygame.font.Font("img/GAMEDAY.ttf", size)

def play():   # ตรวจสอบว่าตำแหน่งของเมาส์อยู่ภายในขอบเขตของปุ่มหรือไม่
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()

def main_menu(): # สร้างหน้าจอเมนู
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(130).render("CIRCLE-MAN", True, "#FF9966")
        MENU_RECT = MENU_TEXT.get_rect(center=(820, 300))
        # สร้างปุ่ม play และ quit
        PLAY_BUTTON = Button(image=pygame.image.load("img/menu_inv_button.png"), pos=(820, 500),     
                            text_input="PLAY", font=get_font(50), base_color="#FF9966", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("img/menu_inv_button.png"), pos=(820, 650), 
                            text_input="QUIT", font=get_font(50), base_color="#FF9966", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:   # ถ้าคลิกปุ่ม play จะหยุดเพลงพื้นหลังและจะเริ่มเกม
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.mixer.music.stop()
                    start_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS): # ถ้าคลิกปุ่ม quit จะปิดเกม
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main_menu()