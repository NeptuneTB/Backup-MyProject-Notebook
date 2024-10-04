import numpy as np
import json

def get_edge_coordinates(edge_image):
    # หาพิกัดของพิกเซลที่เป็นขอบ
    edge_coordinates = np.column_stack(np.where(edge_image > 0))
    return edge_coordinates

# ฟังก์ชันสำหรับเก็บพิกัดจุดขอบลงในไฟล์ JSON
def save_edge_coordinates_to_json(edge_coords, filename='pointer.json'):
    # เตรียมข้อมูลในรูปแบบที่เหมาะสม
    edges_data = {"edges": [{"x": int(x), "y": int(y)} for (x, y) in edge_coords]}

    # บันทึกลงไฟล์ .json
    with open(filename, 'w') as f:
        json.dump(edges_data, f, indent=4)

    print(f"บันทึกพิกัดจุดขอบลงในไฟล์ {filename} สำเร็จ")

def load_edge_coordinates(filename='pointer.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    pointX = [point['x'] for point in data['edges']]
    pointY = [point['y'] for point in data['edges']]
    return pointX, pointY