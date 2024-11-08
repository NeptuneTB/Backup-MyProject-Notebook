import serial
import time

def send_command(ser, command):
    """
    ส่งคำสั่งไปยัง switch และรอการตอบกลับ
    """
    ser.write((command + '\r\n').encode())
    time.sleep(1)
    return ser.read(ser.in_waiting).decode()

def configure_switch(port='COM1'):
    try:
        # เปิดการเชื่อมต่อ serial แบบพื้นฐาน
        ser = serial.Serial(port=port, timeout=1)

        # รายการคำสั่งทั้งหมด
        commands = [
            'enable',
            'config term',
            'hostname R1',
            'interface g0/0',
            'no shutdown',
            'interface g0/0.1',
            'encapsulation dot1q 1',
            'ip address 172.17.1.1 255.255.255.0',
            'interface g0/0.10',
            'encapsulation dot1q 10',
            'ip address 172.17.10.1 255.255.255.0',
            'interface g0/0.20',
            'encapsulation dot1q 20',
            'ip address 172.17.20.1 255.255.255.0',
            'interface g0/0.30',
            'encapsulation dot1q 30',
            'ip address 172.17.30.1 255.255.255.0',
            'interface g0/0.99',
            'encapsulation dot1q 99 native',
            'ip address 172.17.99.1 255.255.255.0',
            'exit',
            'interface g0/1',
            'ip address 172.17.50.1 255.255.255.0',
            'description server interface',
            'no shutdown'
        ]

        # ส่งแต่ละคำสั่งไปยัง switch
        for command in commands:
            print(f"กำลังส่งคำสั่ง: {command}")
            response = send_command(ser, command)
            print(f"การตอบกลับ: {response}")
            time.sleep(1)

        # ปิดการเชื่อมต่อ
        ser.close()
        print("ตั้งค่าเสร็จสมบูรณ์")

    except serial.SerialException as e:
        print(f"เกิดข้อผิดพลาดในการเปิด port: {e}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    # เรียกใช้ฟังก์ชันโดยระบุแค่ port
    configure_switch(port='COM1')  # เปลี่ยน COM1 เป็น port ที่ใช้งานจริง