# mqtt_publisher.py
import paho.mqtt.client as mqtt
import json

broker = "localhost"
port = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def publish_message(topic, message):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker, port, 60)
    
    client.loop_start()

    # ส่งข้อความที่ได้รับมา
    payload = json.dumps(message)
    client.publish(topic, payload)

    client.loop_stop()
