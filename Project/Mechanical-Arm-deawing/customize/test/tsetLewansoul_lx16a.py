import serial
import time
import lewansoul_lx16a

ser = lewansoul_lx16a.ServoController(serial.Serial(port='COM4', baudrate=115200, timeout=1))

servo_id1 = 1
servo_id2 = 2
servo_id3 = 3
servo_id4 = 4

ser.move(servo_id1, 100)
time.sleep(1)

ser.move(servo_id1, 200)
time.sleep(1)

ser.move(servo_id1, 300)
time.sleep(1)

# ser.motor_off(servo_id2)