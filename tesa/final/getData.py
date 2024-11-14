import requests

# ดูรายการข้อมูลทั้งหมด
response = requests.get(
    "http://localhost:8080/list-data",
    headers={"Authorization": "Bearer list_ab2355de4ba54c09f0f70373a4c0c18058689a287251fd842f9ba7ed39652192"}
)

if response.status_code == 200:
    data = response.json()["data"]
    for item in data:
        print(f"Timestamp: {item['timestamp']}")
        print(f"Data: {item['data']}")
        print()
else:
    print("Error listing data:", response.json())

# ดูรายการข้อมูลของ device_001
response = requests.get(
    "http://localhost:8080/list-data?device_id=device_001",
    headers={"Authorization": "Bearer list_ab2355de4ba54c09f0f70373a4c0c18058689a287251fd842f9ba7ed39652192"}
)

if response.status_code == 200:
    data = response.json()["data"]
    for item in data:
        print(f"Timestamp: {item['timestamp']}")
        print(f"Data: {item['data']}")
        print()
else:
    print("Error listing data:", response.json())