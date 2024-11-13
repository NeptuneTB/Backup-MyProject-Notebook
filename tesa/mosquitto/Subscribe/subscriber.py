# mqtt_subscriber.py
import paho.mqtt.client as mqtt
import json
from manage.database import save_data

broker = "localhost"
port = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    # Decode the MQTT message payload (bytes to string)
    message = msg.payload.decode()

    # พยายามแปลงข้อความที่ได้รับเป็น JSON
    try:
        # หากเป็น JSON ให้แปลงเป็น dict
        data = json.loads(message)
        print(f"Received JSON message: {data}")
    except json.JSONDecodeError:
        # หากไม่ใช่ JSON ก็เก็บข้อความเป็น string ในรูปแบบ dict
        data = {"message": message}
        print(f"Received message as plain string: {message}")

    # ส่งข้อมูลที่แปลงแล้วไปบันทึกในฐานข้อมูล MongoDB
    save_data(data)

def subscribe_to_topic(topic):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.subscribe(topic)

    client.loop_forever()
