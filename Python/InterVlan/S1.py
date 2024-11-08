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
            'hostname S1',
            'no ip domain-lookup',
            'ip default-gateway 172.17.99.1',
            'exit',
            'vtp mode server',
            'vtp domain Lab6',
            'interface ra f0/1-5',
            'switchport mode trunk',
            'switchport trunk native vlan 99',
            'no shutdown',
            'exit',
            'vlan 99',
            'name management',
            'vlan 10',
            'name faculty-staff',
            'vlan 20',
            'name students',
            'vlan 30',
            'name guest',
            'exit',
            'interface vlan99',
            'ip address 172.17.99.11 255.255.255.0',
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