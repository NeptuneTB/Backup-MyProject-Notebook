from flask import Flask, request, jsonify, send_from_directory, send_file, after_this_request, make_response
import os
import sqlite3
from datetime import datetime, timedelta
import zipfile
import tempfile
import time
from contextlib import contextmanager

app = Flask(__name__)
UPLOAD_FOLDER = 'audio_files'  # Folder for storing audio files
DATABASE = 'audio_data.sqlite'  # SQLite database file
API_KEY = 'Bearer 601194170c91871f481d9b2cb8030c09df307ebb0236f588896751940709024f'
TEMP_ZIP_FOLDER = os.path.join(UPLOAD_FOLDER, 'zipfile')
# Ensure the temporary directory exists
os.makedirs(TEMP_ZIP_FOLDER, exist_ok=True)

def init_database():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data_size INTEGER NOT NULL,
                device_id TEXT NOT NULL
            );
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        app.logger.error(f"Database initialization error: {str(e)}")

def save_to_database(file_path, timestamp, data_size, device_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audio_files (file_path, timestamp, data_size, device_id)
            VALUES (?, ?, ?, ?)
        ''', (file_path, timestamp, data_size, device_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        app.logger.error(f"Database save error: {str(e)}")

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
        
        
@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
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
    save_to_database(file_path, timestamp, data_size, device_id)

    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/list-audio-files', methods=['GET'])
def list_audio_files():
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT file_path FROM audio_files')
        files = [os.path.basename(row[0]) for row in cursor.fetchall()]
        conn.close()
        return jsonify({"files": files}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Database query error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
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
    """
    Flask endpoint to download all audio files as a ZIP archive.
    Requires API key authentication.
    """
    # ตรวจสอบ API key
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
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
    """Endpoint สำหรับทำความสะอาดไฟล์ชั่วคราวด้วยตนเอง"""
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    cleanup_old_temp_files(TEMP_ZIP_FOLDER, max_age_hours=0)  # ลบทุกไฟล์
    return jsonify({"message": "Cleanup completed"}), 200

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=8080, debug=True)
