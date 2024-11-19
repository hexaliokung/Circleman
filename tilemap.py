import pygame as pg  # นำเข้าโมดูล Pygame สำหรับการจัดการเกม
from settings import *  # นำเข้าค่าการตั้งค่าที่กำหนดไว้ในไฟล์ settings.py

# คลาส Map ใช้สำหรับจัดการแผนที่ของเกม
class Map:
    def __init__(self, filename):
        """
        อ่านไฟล์แผนที่จากไฟล์ .txt แล้วเก็บข้อมูลในรูปแบบของกริด
        """
        self.data = []  # สร้างรายการเพื่อเก็บข้อมูลแผนที่
        with open(filename, "rt") as f:  # เปิดไฟล์แผนที่แบบอ่าน (read text)
            for line in f:  # อ่านทีละบรรทัด
                self.data.append(line.strip())  # ลบช่องว่างและเพิ่มข้อมูลลงใน data
        
        # คำนวณความกว้างและความสูงของแผนที่ในหน่วย Tile
        self.tilewidth = len(self.data[0])  # จำนวนคอลัมน์ในแถวแรก
        self.tileheight = len(self.data)  # จำนวนแถวทั้งหมด
        
        # คำนวณความกว้างและความสูงของแผนที่ในพิกเซล
        self.width = self.tilewidth * TILESIZE  # ความกว้างของแผนที่ในพิกเซล
        self.height = self.tileheight * TILESIZE  # ความสูงของแผนที่ในพิกเซล

# คลาส Camera ใช้สำหรับจัดการมุมมองของกล้องในเกม
class Camera:
    def __init__(self, width, height):
        """
        กำหนดพื้นที่ของกล้องและขนาดของแผนที่
        """
        self.camera = pg.Rect(0, 0, width, height)  # สร้าง Rect เริ่มต้นที่ (0, 0) และมีขนาดเท่ากับแผนที่
        self.width = width  # กำหนดความกว้างของกล้อง
        self.height = height  # กำหนดความสูงของกล้อง

    def apply(self, entity):
        """
        ปรับตำแหน่งของเอนทิตี (วัตถุในเกม) ตามตำแหน่งของกล้อง
        """
        return entity.rect.move(self.camera.topleft)  # เลื่อนตำแหน่งของเอนทิตีตามมุมบนซ้ายของกล้อง

    def apply_rect(self, rect):
        """
        ปรับตำแหน่งของสี่เหลี่ยม (Rect) ตามตำแหน่งของกล้อง
        """
        return rect.move(self.camera.topleft)  # เลื่อนตำแหน่งของ Rect ตามมุมบนซ้ายของกล้อง

    def update(self, target):
        """
        อัปเดตตำแหน่งของกล้องให้ตามติดกับเป้าหมาย (target)
        """
        # คำนวณตำแหน่งใหม่ของกล้อง โดยให้เป้าหมายอยู่ตรงกลางของหน้าจอ
        x = -target.rect.centerx + WIDTH // 2  # ตำแหน่ง x ของกล้อง
        y = -target.rect.centery + HEIGHT // 2  # ตำแหน่ง y ของกล้อง

        # จำกัดการเลื่อนของกล้องไม่ให้ออกนอกขอบแผนที่
        x = min(0, x)  # ขอบซ้าย
        y = min(0, y)  # ขอบบน
        x = max(-(self.width - WIDTH), x)  # ขอบขวา
        y = max(-(self.height - HEIGHT), y)  # ขอบล่าง

        # อัปเดตตำแหน่งของกล้อง
        self.camera = pg.Rect(x, y, self.width, self.height)  # สร้าง Rect ใหม่ให้กล้องเลื่อนตามเป้าหมาย