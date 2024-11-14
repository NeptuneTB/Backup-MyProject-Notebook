from flask import Flask, request, jsonify, send_from_directory, send_file, after_this_request, make_response
import os
import sqlite3
from datetime import datetime
import zipfile
import tempfile
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'audio_files'  # โฟลเดอร์สำหรับเก็บไฟล์เสียง
DATABASE = 'audio_data.sqlite'  # ไฟล์ฐานข้อมูล SQLite
API_KEY = 'Bearer 601194170c91871f481d9b2cb8030c09df307ebb0236f588896751940709024f'
TEMP_ZIP_FOLDER = os.path.join(UPLOAD_FOLDER, 'zipfile')
# ตรวจสอบและสร้างโฟลเดอร์ชั่วคราวหากไม่มี
os.makedirs(TEMP_ZIP_FOLDER, exist_ok=True)

def init_database():
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


def save_to_database(file_path, timestamp, data_size, device_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audio_files (file_path, timestamp, data_size, device_id)
        VALUES (?, ?, ?, ?)
    ''', (file_path, timestamp, data_size, device_id))
    conn.commit()
    conn.close()
    
    
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


# ฟังก์ชันตรวจสอบและดึงรายชื่อไฟล์ทั้งหมดในเซิร์ฟเวอร์
@app.route('/list-audio-files', methods=['GET'])
def list_audio_files():
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT file_path FROM audio_files')
    files = [os.path.basename(row[0]) for row in cursor.fetchall()]  # เก็บชื่อไฟล์ทั้งหมด
    conn.close()

    return jsonify({"files": files}), 200


# ฟังก์ชันดาวน์โหลดไฟล์ตามชื่อไฟล์ที่ต้องการ
@app.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # ตรวจสอบว่าไฟล์นั้นมีอยู่ในเซิร์ฟเวอร์หรือไม่
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.isfile(file_path):
            return jsonify({"error": "File not found"}), 404

        # ส่งไฟล์กลับให้ผู้ใช้
        return send_from_directory(
            UPLOAD_FOLDER,
            filename,
            as_attachment=True  # ตั้งค่าให้ดาวน์โหลดไฟล์
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
    
@app.route('/download-all-audio', methods=['GET'])
def download_all_audio():
    # Verify API key
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Create temporary ZIP file
    temp_zip = tempfile.NamedTemporaryFile(
        dir=TEMP_ZIP_FOLDER,
        suffix=".zip",
        delete=False
    )

    try:
        # Create ZIP archive with all audio files
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(UPLOAD_FOLDER):
                for file in files:
                    # Skip the temporary ZIP file itself
                    if file != os.path.basename(temp_zip.name):
                        file_path = os.path.join(root, file)
                        # Preserve relative path structure in ZIP
                        arc_path = os.path.relpath(file_path, UPLOAD_FOLDER)
                        zipf.write(file_path, arc_path)

        temp_zip.close()

        # Define cleanup function to run after request
        @after_this_request
        def cleanup(response):
            MAX_RETRIES = 3
            RETRY_DELAY = 1  # seconds

            for attempt in range(MAX_RETRIES):
                try:
                    os.unlink(temp_zip.name)
                    app.logger.info(f"Successfully deleted temp ZIP: {temp_zip.name}")
                    break
                except PermissionError:
                    app.logger.warning(
                        f"Permission error deleting temp ZIP (attempt {attempt + 1}/{MAX_RETRIES})"
                    )
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY)
                except Exception as e:
                    app.logger.error(f"Failed to delete temp ZIP: {str(e)}")
                    break
            return response

        # Prepare and send response
        response = make_response(
            send_file(
                temp_zip.name,
                as_attachment=True,
                download_name="audio_files.zip"  # Added explicit download name
            )
        )
        response.headers["Connection"] = "close"
        return response

    except Exception as e:
        app.logger.error(f"Failed to create ZIP archive: {str(e)}")
        # Clean up temp file if it exists
        try:
            os.unlink(temp_zip.name)
        except Exception as cleanup_error:
            app.logger.error(f"Failed to clean up temp ZIP after error: {str(cleanup_error)}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=8080, debug=True)

