import serial
import lewansoul_lx16a
import tkinter as tk
from tkinter import ttk

# สร้าง object Serial เพื่อเชื่อมต่อกับพอร์ต COM
ser = lewansoul_lx16a.ServoController(serial.Serial('COM4', 115200, timeout=1))

# ฟังก์ชันเคลื่อนเซอร์โว
def move_servo(servo_id, position):
    # ส่งคำสั่งไปยังเซอร์โวเพื่อเคลื่อนที่ไปยังตำแหน่งที่กำหนด
    ser.move(servo_id, position)

# ฟังก์ชันดึงตำแหน่งของเซอร์โวปัจจุบัน
def get_servo_position(servo_id):
    # อ่านตำแหน่งจากเซอร์โว (ตำแหน่งเป็นค่า integer)
    return ser.get_position(servo_id)

# สร้างหน้าจอ GUI ด้วย Tkinter
class ServoControlApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lewansoul LX-16A Servo Control")
        self.geometry("400x600")

        # สร้าง Slider และช่องกรอกตำแหน่งสำหรับเซอร์โวแต่ละตัว
        for servo_id in range(1, 5):
            self.create_servo_slider(servo_id)

    def create_servo_slider(self, servo_id):
        # สร้าง Label สำหรับแสดงเซอร์โวแต่ละตัว
        label = ttk.Label(self, text=f"Servo {servo_id} Control")
        label.pack(pady=10)

        # สร้างตัวแสดงตำแหน่ง
        position_label = ttk.Label(self, text="Position: 0")
        position_label.pack(pady=5)

        # ดึงตำแหน่งเริ่มต้นของเซอร์โว
        current_position = get_servo_position(servo_id)

        # สร้าง Slider สำหรับควบคุมเซอร์โว (จาก 0 ถึง 1000) โดยเริ่มจากตำแหน่งปัจจุบัน
        slider = ttk.Scale(self, from_=0, to=1000, orient='horizontal', value=current_position)
        slider.pack(pady=5)

        # สร้างช่องกรอกข้อมูลสำหรับป้อนตัวเลขตำแหน่ง
        entry = ttk.Entry(self)
        entry.pack(pady=5)
        entry.insert(0, str(current_position))  # ใส่ตำแหน่งปัจจุบันใน entry

        # อัปเดตตำแหน่งใน label เมื่อเลื่อน slider
        def update_position(event):
            position = int(slider.get())
            position_label.config(text=f"Position: {position}")
            entry.delete(0, tk.END)  # ลบข้อมูลเก่าในช่องกรอก
            entry.insert(0, str(position))  # ใส่ข้อมูลใหม่ในช่องกรอก
            move_servo(servo_id, position)

        # เมื่อมีการปรับ slider ให้ส่งคำสั่งไปยังเซอร์โวและแสดงตำแหน่ง
        slider.bind("<Motion>", update_position)

        # ฟังก์ชันอัปเดตตำแหน่งจากการกรอกตัวเลข
        def set_position_from_entry(event):
            try:
                position = int(entry.get())  # ดึงค่าจากช่องกรอก
                if 0 <= position <= 1000:  # ตรวจสอบว่าค่าตำแหน่งอยู่ในช่วงที่ถูกต้อง
                    slider.set(position)  # ปรับ slider ตามตัวเลขที่ป้อน
                    position_label.config(text=f"Position: {position}")  # อัปเดต label
                    move_servo(servo_id, position)  # ส่งตำแหน่งไปยังเซอร์โว
                else:
                    print("ตำแหน่งเกินขอบเขต")
            except ValueError:
                print("กรุณากรอกตัวเลขที่ถูกต้อง")

        # เมื่อกด Enter ในช่องกรอกจะส่งตำแหน่งไปยังเซอร์โว
        entry.bind("<Return>", set_position_from_entry)

        # แสดงตำแหน่งเริ่มต้นใน label
        position_label.config(text=f"Position: {current_position}")

# สร้างอินสแตนซ์ของแอพพลิเคชันและเริ่มการทำงาน
if __name__ == "__main__":
    app = ServoControlApp()
    app.mainloop()
