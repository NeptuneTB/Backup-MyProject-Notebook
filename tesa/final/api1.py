from flask import Flask, request, jsonify, send_from_directory, send_file, after_this_request, make_response
import os
import sqlite3
from datetime import datetime, timedelta
import zipfile
import tempfile
import time
from contextlib import contextmanager
import logging
from werkzeug.utils import secure_filename
import re
from functools import wraps
import shutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'audio_files'
DATABASE = 'audio_data.sqlite'
TEMP_ZIP_FOLDER = os.path.join(UPLOAD_FOLDER, 'zipfile')
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# กำหนด API keys แยกตาม endpoint
API_KEYS = {
    'upload': os.getenv('upload'),
    'list': os.getenv('list'),
    'download': os.getenv('download'),
    'download_all': os.getenv('download_all')
}

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# สร้างโฟลเดอร์ที่จำเป็น
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_ZIP_FOLDER, exist_ok=True)

def require_api_key(key_type):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('Authorization')
            if not api_key or api_key != API_KEYS.get(key_type):
                logger.warning(f"Unauthorized access attempt to {request.path} with key: {api_key}")
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    return secure_filename(filename)

def validate_device_id(device_id):
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', device_id))

def cleanup_old_temp_files(temp_dir, max_age_hours=1):
    """ลบไฟล์ ZIP ชั่วคราวที่เก่ากว่า 1 ชั่วโมง"""
    try:
        now = datetime.now()
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if filename.endswith('.zip'):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if now - file_modified > timedelta(hours=max_age_hours):
                    try:
                        os.remove(filepath)
                        logger.info(f"Deleted old temp file: {filepath}")
                    except Exception as e:
                        logger.error(f"Failed to delete temp file {filepath}: {e}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        conn.close()

def init_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data_size INTEGER NOT NULL,
                device_id TEXT NOT NULL,
                file_hash TEXT,
                UNIQUE(file_path, device_id)
            );
        ''')
        conn.commit()

@app.route('/upload-audio', methods=['POST'])
@require_api_key('upload')
def upload_audio():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        device_id = request.form.get('device_id', '')
        if not device_id or not validate_device_id(device_id):
            return jsonify({"error": "Invalid device ID"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400

        filename = sanitize_filename(file.filename)
        if not filename:
            return jsonify({"error": "Invalid filename"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # ตรวจสอบว่าไฟล์มีอยู่แล้วหรือไม่
        if os.path.exists(file_path):
            return jsonify({"error": "File already exists"}), 409

        file.save(file_path)
        
        timestamp = datetime.now().isoformat()
        data_size = os.path.getsize(file_path)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audio_files (file_path, timestamp, data_size, device_id)
                VALUES (?, ?, ?, ?)
            ''', (file_path, timestamp, data_size, device_id))
            conn.commit()

        logger.info(f"File uploaded successfully: {filename} by device: {device_id}")
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "size": data_size,
            "timestamp": timestamp
        }), 200

    except Exception as e:
        logger.error(f"Error in upload_audio: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/list-audio-files', methods=['GET'])
@require_api_key('list')
def list_audio_files():
    try:
        device_id = request.args.get('device_id')
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if device_id:
                cursor.execute('''
                    SELECT file_path, timestamp, data_size, device_id 
                    FROM audio_files 
                    WHERE device_id = ?
                    ORDER BY timestamp DESC
                ''', (device_id,))
            else:
                cursor.execute('''
                    SELECT file_path, timestamp, data_size, device_id 
                    FROM audio_files 
                    ORDER BY timestamp DESC
                ''')
            
            files = [{
                "filename": os.path.basename(row['file_path']),
                "timestamp": row['timestamp'],
                "size": row['data_size'],
                "device_id": row['device_id']
            } for row in cursor.fetchall()]

        logger.info(f"Audio files listed successfully for device: {device_id if device_id else 'all'}")
        return jsonify({"files": files}), 200

    except Exception as e:
        logger.error(f"Error in list_audio_files: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/download-audio/<filename>', methods=['GET'])
@require_api_key('download')
def download_audio(filename):
    try:
        filename = sanitize_filename(filename)
        if not filename:
            return jsonify({"error": "Invalid filename"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.isfile(file_path):
            return jsonify({"error": "File not found"}), 404

        logger.info(f"File downloaded: {filename}")
        return send_from_directory(
            UPLOAD_FOLDER,
            filename,
            as_attachment=True,
            max_age=0
        )

    except Exception as e:
        logger.error(f"Error in download_audio: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    

@contextmanager
def create_temp_zip():
    """สร้างไฟล์ ZIP ชั่วคราว"""
    temp_file = tempfile.NamedTemporaryFile(
        dir=TEMP_ZIP_FOLDER,
        suffix='.zip',
        delete=False
    )
    try:
        yield temp_file
    finally:
        if os.path.exists(temp_file.name):
            try:
                os.remove(temp_file.name)
            except Exception as e:
                logger.error(f"Failed to delete temp file: {e}")


@app.route('/download-all-audio', methods=['GET'])
@require_api_key('download_all')
def download_all_audio():
    try:
        # ทำความสะอาดไฟล์ ZIP เก่า
        cleanup_old_temp_files(TEMP_ZIP_FOLDER)

        # ดึงข้อมูล device_id จาก query parameter (ถ้ามี)
        device_id = request.args.get('device_id')
        
        # ดึงรายการไฟล์จากฐานข้อมูล
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if device_id:
                cursor.execute('''
                    SELECT file_path, device_id 
                    FROM audio_files 
                    WHERE device_id = ?
                ''', (device_id,))
            else:
                cursor.execute('SELECT file_path, device_id FROM audio_files')
            
            files = cursor.fetchall()

        if not files:
            return jsonify({"error": "No audio files found"}), 404

        # สร้างไฟล์ ZIP
        with create_temp_zip() as temp_zip:
            with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_record in files:
                    file_path = file_record['file_path']
                    device_folder = file_record['device_id']
                    
                    if os.path.exists(file_path):
                        # เก็บไฟล์ในโฟลเดอร์ตาม device_id
                        arc_name = os.path.join(
                            device_folder,
                            os.path.basename(file_path)
                        )
                        zipf.write(file_path, arc_name)

            # สร้างชื่อไฟล์ที่จะดาวน์โหลด
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            download_name = f"audio_files_{timestamp}.zip"
            if device_id:
                download_name = f"audio_files_{device_id}_{timestamp}.zip"

            # ส่งไฟล์กลับไป
            response = send_file(
                temp_zip.name,
                mimetype='application/zip',
                as_attachment=True,
                download_name=download_name
            )

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(temp_zip.name)
                except Exception as e:
                    logger.error(f"Error cleaning up temp file: {e}")
                return response

            logger.info(f"Successfully created ZIP file for download: {download_name}")
            return response

    except Exception as e:
        logger.error(f"Error in download_all_audio: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=8080)