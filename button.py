# button.py make by Tin

# สร้างคลาส Button
class Button():

    # pos = ตำแหน่ง text_input = ข้อความที่รับมา,
    # font = font ที่แสดง, base_color = สีปกติของข้อความในปุ่ม, hovering_color = สีของข้อความเมื่อเมาส์ชี้อยู่เหนือปุ่ม
    def __init__(self, pos, text_input, font, base_color, hovering_color):

        # กำหนดตำแหน่งในแกน x และ y ของปุ่ม
        self.x_pos = pos[0]  # ตำแหน่งปุ่มในแกน x
        self.y_pos = pos[1]  # ตำแหน่งปุ่มในแกน y
        
        # ฟอนต์ของข้อความที่จะแสดงบนปุ่ม (Font Object)
        self.font = font  # ฟอนต์ที่ใช้สร้างข้อความบนปุ่ม
        
        # กำหนดสีพื้นฐาน (เมื่อไม่ได้ชี้เมาส์) และสีเมื่อชี้เมาส์
        self.base_color, self.hovering_color = base_color, hovering_color  # base_color: สีปกติ, hovering_color: สีเมื่อชี้เมาส์
        
        # ข้อความที่จะใช้แสดงบนปุ่ม (Text Input)
        self.text_input = text_input  # ข้อความที่จะแสดง เช่น "START", "EXIT", หรือ "PLAY"
        
        # สร้างพื้นผิวของข้อความ (Text Surface) สำหรับแสดงข้อความโดยใช้ฟอนต์และสีพื้นฐาน
        self.text = self.font.render(self.text_input, True, self.base_color)  
        # self.text คือพื้นผิว (Surface) ที่สามารถวาดลงบนหน้าจอได้
        
        # สร้างกรอบ (Rect) รอบข้อความ เพื่อใช้กำหนดตำแหน่งและตรวจจับการคลิก
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  
        # กำหนดตำแหน่งกรอบให้อยู่ตรงกลางที่ (self.x_pos, self.y_pos)

    def update(self, screen):
        # วาดข้อความบนหน้าจอ ที่ตำแหน่งที่กำหนดโดย self.text_rect
        screen.blit(self.text, self.text_rect)

    # ตรวจจับการชี้
    def checkForInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    # เปลี่ยนสีข้อความเมื่อชี้
    def changeColor(self, position):

        # ตรวจสอบตำแหน่งเมาส์ที่ได้รับและเปลี่ยนสีข้อความในปุ่มตามสถานะ
        # ตรวจสอบว่าตำแหน่ง x และ y ของเมาส์อยู่ในกรอบของปุ่มหรือไม่
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            # ถ้าเมาส์อยู่ภายในกรอบของปุ่ม
            # สร้างพื้นผิวข้อความใหม่ (self.text) ด้วยสี hovering_color
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            # ถ้าเมาส์ไม่ได้อยู่ในกรอบของปุ่ม
            # สร้างพื้นผิวข้อความใหม่ (self.text) ด้วยสี base_color
            # base_color คือสีปกติของข้อความบนปุ่ม
            self.text = self.font.render(self.text_input, True, self.base_color)