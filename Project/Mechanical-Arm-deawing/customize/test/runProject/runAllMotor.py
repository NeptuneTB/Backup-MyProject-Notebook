import serial
import time
import lewansoul_lx16a
import numpy as np
from convertImage.imagePointer import load_edge_coordinates

ser = lewansoul_lx16a.ServoController(serial.Serial(port='COM4', baudrate=115200, timeout=1))
serial = serial.Serial(port='COM3', baudrate=115200, timeout=1)

# กำหนดขอบเขตสำหรับเซอร์โวแต่ละตัว (แยกตาม ID)
servo_limits = {
    1: {'min_position': 390, 'max_position': 500},  # ขอบเขตสำหรับเซอร์โว ID 1
    2: {'min_position': 50, 'max_position': 380},  # ขอบเขตสำหรับเซอร์โว ID 2
    3: {'min_position': 0, 'max_position': 500},  # ขอบเขตสำหรับเซอร์โว ID 3
    4: {'min_position': 700, 'max_position': 750}   # ขอบเขตสำหรับเซอร์โว ID 4
}

# ฟังก์ชันเคลื่อนเซอร์โวแต่ละตัว โดยตรวจสอบขอบเขตก่อน
def move_servo_in_limit(servo_id, position):
    # ตรวจสอบว่ามีขอบเขตสำหรับเซอร์โวตัวนี้ใน dictionary หรือไม่
    if servo_id in servo_limits:
        min_position = servo_limits[servo_id]['min_position']
        max_position = servo_limits[servo_id]['max_position']

        # ตรวจสอบว่าตำแหน่งอยู่ภายในขอบเขต
        if position < min_position:
            position = min_position
        elif position > max_position:
            position = max_position
    else:
        print(f"Servo ID {servo_id} ไม่มีขอบเขตที่กำหนดไว้")
        return

    # เคลื่อนเซอร์โวไปยังตำแหน่งที่กำหนด (หลังจากตรวจสอบขอบเขต)
    ser.move(servo_id, position)

def logicMotor():
    pointX, pointY = load_edge_coordinates()

    for x, y in zip(pointX, pointY):
        print(f"x = {x}, y = {y}")


if __name__ == "__main__":
    logicMotor()