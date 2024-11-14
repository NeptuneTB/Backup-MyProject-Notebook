import json
import requests

# ตัวอย่างข้อมูลเซ็นเซอร์พร้อม device_id
sensor_data = {
    "device_id": "device_001",
    "Energy Consumption": {"Power": 94.31833772751385},
    "Voltage": {
        "L1-GND": 228.74109932030456,
        "L2-GND": 227.2177735314532,
        "L3-GND": 234.9266839023613
    },
    "Pressure": 19.92381106280107,
    "Force": 30.675302431862935,
    "Cycle Count": 1697,
    "Position of the Punch": 107.70437351552874
}

# ส่งข้อมูลไปยัง API โดยใช้ json
response = requests.post(
    "http://localhost:8080/upload-data",
    headers={"Authorization": "Bearer data_2a85221af25e55f1675f0be90c686530d4cb86186ef7c684aba47d5ae00e011f"},
    json=sensor_data
)

if response.status_code == 200:
    print("Data uploaded successfully!")
else:
    print("Error uploading data:", response.json())
