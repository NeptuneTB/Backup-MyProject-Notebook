import serial.tools.list_ports
import serial
import time

# ports = serial.tools.list_ports.comports()
# portlist = []
#
# for i in ports:
#     portlist.append(str(i))
#     print(str(i))
#
# com = input("Select Com Port For Arduino: ")
#
# for i in range(len(portlist)):
#     if portlist[i].startswith("COM" + str(com)):
#         use = "COM" + str(com)
#         print(use)

ser = serial.Serial('COM3', 9600, timeout=1)
# ser.baudrate = 9600
# ser.port = use
# ser.timeout(1)
# ser.open()

# กำหนดพอร์ตอนุกรมที่ Arduino เชื่อมต่ออยู่
# arduino_port = 'COM3'  # เปลี่ยนเป็นพอร์ตที่ Arduino เชื่อมต่ออยู่
# baud_rate = 9600  # ความเร็วในการสื่อสาร Serial

# สร้างการเชื่อมต่อกับ Arduino
# ser = serial.Serial('COM3', 9600)
# time.sleep(2)  # รอให้การเชื่อมต่อเสร็จสมบูรณ์


# def send_command(command):
#     ser.write((command + '\n').encode('UTF-8'))


# while True:
#      command = input("Enter command (s, b, q): ")
#      if command in ["s", "b", "q"]:
#          send_command(command)
#      else:
#          print("Invalid command.")
# start = 's'
# back = 'b'
# stop = 'q'
#
# for i in range(1, 11):
#     # send_command(start)
#     ser.write(start.encode('utf-8'))
#     time.sleep(2)
#     print(f"Start = {i}")
# for i in range(1, 11):
#     # send_command(back)
#     ser.write(back.encode('utf-8'))
#     time.sleep(2)
#     print(f"Back = {i}")
# # send_command(stop)
# ser.write(stop.encode('utf-8'))
# print("Stop")

def send_command(x):
    ser.write(bytearray([byte_value]))  # ส่งค่าไบต์
    # ser.write(bytes(x, 'utf-8'))
    # print(serial)
    time.sleep(1)
    data = ser.readline().decode('utf-8').strip()
    return data

while True:
    byte_input = input("Enter a byte value (0-255) or 'q' to quit: ")
    if byte_input.lower() == 'q':
        ser.close()
        break
    try:
        byte_value = int(byte_input)
        if 0 <= byte_value <= 255:
            response = send_command(byte_value)
            print(response)
        else:
            print("Please enter a value between 0 and 255.")
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

    # command = input("Arduino Command (L/R/q): ")
    # value = send_command(command)
    # # string = str(value, encoding='utf-8')
    # # print(string)
    #
    # if command == "q":
    #     ser.close()
    #     exit()


# except KeyboardInterrupt:
#     print("Exiting program.")
