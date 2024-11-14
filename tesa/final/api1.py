from flask import Flask, request, jsonify, send_from_directory, send_file, after_this_request, make_response
import os
import sqlite3
from datetime import datetime, timedelta
import zipfile
import tempfile
import time
from contextlib import contextmanager
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'audio_files'  # Folder for storing audio files
DATABASE = 'audio_data.sqlite'  # SQLite database file
TEMP_ZIP_FOLDER = os.path.join(UPLOAD_FOLDER, 'zipfile')
# Ensure the temporary directory exists
os.makedirs(TEMP_ZIP_FOLDER, exist_ok=True)

ENDPOINT_API_KEYS = {
    "upload_audio": os.getenv('upload'),
    "list_audio_files": os.getenv('list'),
    "download_audio": os.getenv('download'),
    "download_all_audio": os.getenv('download_all'),
    "manual_cleanup": os.getenv('manual_cleanup'),
    "upload_sensor_data": os.getenv('data'),
    "get_sensor_data": os.getenv('listdata')
}


def init_database():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # สร้างตารางสำหรับไฟล์เสียง
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data_size INTEGER NOT NULL,
                device_id TEXT
            );
        ''')
        
        # สร้างตารางสำหรับ sensor data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                device_id NULL,
                data JSON NOT NULL
            );
        ''')
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        app.logger.error(f"Database initialization error: {str(e)}")

def save_to_database(table, **data):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if table == 'audio_files':
            cursor.execute('''
                INSERT INTO audio_files (file_path, timestamp, data_size, device_id)
                VALUES (?, ?, ?, ?)
            ''', (
                data['file_path'], 
                data['timestamp'], 
                data['data_size'], 
                data.get('device_id')  # device_id อาจเป็น None
            ))

        elif table == 'sensor_data':
            cursor.execute('''
                INSERT INTO sensor_data (timestamp, device_id, data)
                VALUES (?, ?, ?)
            ''', (
                data['timestamp'], 
                data.get('device_id'),  # device_id อาจเป็น None
                json.dumps(data['data'])
            ))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        app.logger.error(f"Database save error: {str(e)}")


def validate_api_key(endpoint):
    api_key = request.headers.get('Authorization')
    # app.logger.info(f"Received API key: {api_key}")
    return api_key == ENDPOINT_API_KEYS.get(endpoint)


# สร้าง context manager สำหรับจัดการไฟล์ชั่วคราว
@contextmanager
def managed_temp_file(suffix=".zip", directory=None):
    temp_file = tempfile.NamedTemporaryFile(
        dir=directory,
        suffix=suffix,
        delete=False
    )
    try:
        yield temp_file
    finally:
        temp_file.close()
        if os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception as e:
                app.logger.error(f"Failed to delete temp file in context manager: {e}")

# เพิ่มฟังก์ชันทำความสะอาดไฟล์เก่า
def cleanup_old_temp_files(temp_dir, max_age_hours=1):
    """ลบไฟล์ชั่วคราวที่เก่ากว่าเวลาที่กำหนด"""
    try:
        now = datetime.now()
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if filename.endswith('.zip'):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if now - file_modified > timedelta(hours=max_age_hours):
                    try:
                        os.unlink(filepath)
                        app.logger.info(f"Deleted old temp file: {filepath}")
                    except Exception as e:
                        app.logger.error(f"Failed to delete old temp file {filepath}: {e}")
    except Exception as e:
        app.logger.error(f"Error during cleanup of old temp files: {e}")
        

@app.route('/upload-sensor-data', methods=['POST'])
def upload_sensor_data():
    if not validate_api_key('upload_sensor_data'):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        timestamp = datetime.now().isoformat()
        device_id = data.get('device_id', 'unknown_device')
        sensor_data = data.get('data', {})

        save_to_database('sensor_data', timestamp=timestamp, device_id=device_id, data=sensor_data)
        return jsonify({"message": "Sensor data uploaded successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error uploading sensor data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
        
 
@app.route('/get-sensor-data', methods=['GET'])
def get_sensor_data():
    """Endpoint สำหรับดึงข้อมูล sensor data"""
    if not validate_api_key('get_sensor_data'):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, timestamp, device_id, data FROM sensor_data')
        sensor_data = [
            {
                "id": row[0],
                "timestamp": row[1],
                "device_id": row[2],
                "data": json.loads(row[3])  # แปลงจาก JSON string เป็น dictionary
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        return jsonify({"sensor_data": sensor_data}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Database query error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
 
        
@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if not validate_api_key('upload_audio'):
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file.save(file_path)

    timestamp = datetime.now().isoformat()
    data_size = os.path.getsize(file_path)
    device_id = request.form.get('device_id', 'unknown_device')
    save_to_database(
        table='audio_files',
        file_path=file_path,
        timestamp=timestamp,
        data_size=data_size,
        device_id=device_id
    )


    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/list-audio-files', methods=['GET'])
def list_audio_files():
    if not validate_api_key('list_audio_files'):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, file_path, timestamp, data_size, device_id FROM audio_files')
        audio_files = [
            {
                "id": row[0],
                "file_path": row[1],
                "timestamp": row[2],
                "data_size": row[3],
                "device_id": row[4] if row[4] is not None else "unknown_device"  # ใช้ "unknown_device" หาก device_id เป็น NULL
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        return jsonify({"audio_files": audio_files}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Database query error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    

@app.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    if not validate_api_key('download_audio'):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.isfile(file_path):
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(
            UPLOAD_FOLDER,
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/download-all-audio', methods=['GET'])
def download_all_audio():
    if not validate_api_key('download_all_audio'):
        return jsonify({"error": "Unauthorized"}), 401

    # ทำความสะอาดไฟล์เก่าก่อน
    cleanup_old_temp_files(TEMP_ZIP_FOLDER)

    try:
        # ใช้ context manager จัดการไฟล์ชั่วคราว
        with managed_temp_file(directory=TEMP_ZIP_FOLDER) as temp_zip:
            # สร้างไฟล์ ZIP
            with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(UPLOAD_FOLDER):
                    for file in files:
                        if file.endswith(('.mp3', '.wav', '.ogg')):  # เพิ่มการกรองไฟล์เสียง
                            file_path = os.path.join(root, file)
                            arc_path = os.path.relpath(file_path, UPLOAD_FOLDER)
                            zipf.write(file_path, arc_path)

            # สร้าง response
            try:
                response = make_response(
                    send_file(
                        temp_zip.name,
                        as_attachment=True,
                        download_name=f"audio_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        max_age=0
                    )
                )
                response.headers["Connection"] = "close"
                response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                
                # เพิ่ม callback สำหรับลบไฟล์หลังส่ง response
                @after_this_request
                def delete_temp_file(response):
                    def delayed_delete():
                        max_retries = 5
                        for i in range(max_retries):
                            try:
                                if os.path.exists(temp_zip.name):
                                    os.unlink(temp_zip.name)
                                    app.logger.info(f"Successfully deleted temp file: {temp_zip.name}")
                                return
                            except Exception as e:
                                if i == max_retries - 1:
                                    app.logger.error(f"Final attempt to delete temp file failed: {e}")
                                else:
                                    app.logger.warning(f"Retry {i+1} failed to delete temp file: {e}")
                                    time.sleep(1)
                    
                    # เริ่ม thread ใหม่สำหรับลบไฟล์
                    from threading import Thread
                    Thread(target=delayed_delete).start()
                    return response

                return response

            except Exception as e:
                app.logger.error(f"Error sending file: {e}")
                raise

    except Exception as e:
        app.logger.error(f"Error creating ZIP file: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# เพิ่ม endpoint สำหรับทำความสะอาดไฟล์เก่าด้วยตนเอง
@app.route('/cleanup-temp-files', methods=['POST'])
def manual_cleanup():
    if not validate_api_key('manual_cleanup'):
        return jsonify({"error": "Unauthorized"}), 401
    
    cleanup_old_temp_files(TEMP_ZIP_FOLDER, max_age_hours=0)  # ลบทุกไฟล์
    return jsonify({"message": "Cleanup completed"}), 200

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=8080, debug=True)
