# app.py
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from Publish.publisher import publish_message
from Subscribe.subscriber import subscribe_to_topic
from manage.database import collection

app = Flask(__name__)
socketio = SocketIO(app)

# การเริ่มต้น subscriber ใน Thread แยก
def start_subscriber(topic):
    subscriber_thread = threading.Thread(target=subscribe_to_topic, args=(topic,))
    subscriber_thread.start()

# เมื่อผู้ใช้ส่ง topic ผ่าน WebSocket
@socketio.on('set_topic')
def handle_topic(data):
    topic = data.get('topic')
    
    if topic:
        print(f"New topic: {topic}")
        
        # เริ่มต้น subscriber สำหรับ topic ที่ผู้ใช้กำหนด
        start_subscriber(topic)

@socketio.on('send_message')
def handle_message(data):
    topic = data.get('topic')
    message = data.get('message')
    
    if topic and message:
        print(f"Publishing to {topic}: {message}")
        
        # ส่งข้อความไปยัง MQTT broker
        publish_message(topic, message)

@app.route('/')
def index():
    # ดึงข้อมูลล่าสุดจาก MongoDB
    data = list(collection.find().sort('_id', -1).limit(1))
    if data:
        data = data[0]
    else:
        data = {}

    return render_template('index.html', data=data)

@app.route('/api/data')
def api_data():
    # ดึงข้อมูลล่าสุดจาก MongoDB
    data = list(collection.find().sort('_id', -1).limit(1))
    if data:
        data = data[0]
    else:
        data = {}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
