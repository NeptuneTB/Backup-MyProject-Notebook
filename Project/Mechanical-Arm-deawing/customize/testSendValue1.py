import serial
import time

# ตั้งค่าพอร์ตและ baud rate
ser = serial.Serial(port='COM3', baudrate=115200, timeout=1)  # เปลี่ยนเป็นพอร์ตที่ถูกต้อง
time.sleep(2)  # รอให้การเชื่อมต่อเสถียร

def send_initial_command():
    command = "start1\n"
    print(f"Sending command: {command.strip()}")  # พิมพ์คำสั่งที่ส่งไป
    ser.write(command.encode())
    time.sleep(1)  # รอให้ Arduino มีเวลาประมวลผลและตอบกลับ
    response = ser.readline().decode('utf-8').strip()
    print(f"Response: {response}")  # พิมพ์การตอบกลับที่ได้รับ
    return response

def send_command(direction, steps):
    command = f"{direction}{steps}\n"
    print(f"Sending command: {command.strip()}")  # พิมพ์คำสั่งที่ส่งไป
    ser.write(command.encode())
    time.sleep(1)  # รอให้ Arduino มีเวลาประมวลผลและตอบกลับ
    response = ser.readline().decode('utf-8').strip()
    print(f"Response: {response}")  # พิมพ์การตอบกลับที่ได้รับ
    return response

def value_output():
    while True:
        direction = input("Enter direction (F/B) or 'q' to quit: ").upper()
        if direction.lower() == 'q':
            ser.close()
            print("Serial connection closed.")
            break
        if direction not in ['F', 'B']:
            print("Invalid direction. Use 'F' for forward or 'B' for backward.")
            continue

        try:
            steps = int(input("Enter number of steps: "))  # ตรวจสอบให้แน่ใจว่า steps เป็นตัวเลข
            response = send_command(direction, steps)
            print(response)
        except ValueError:
            print("Invalid input. Please enter a numeric value for steps.")

if __name__ == "__main__":
    # ส่งคำสั่งเริ่มต้น
    initial_response = send_initial_command()
    if initial_response == "Arduino Ready":
        while True:
            value_output()
    else:
        print("Failed to receive Arduino Ready response")
        ser.close()
