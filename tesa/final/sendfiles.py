import requests

url = 'http://yourserver.com/upload-audio'
file_path = '/path/to/your_audio_file.wav'
api_key = 'YOUR_API_KEY'  # ใส่ API key เพื่อการตรวจสอบสิทธิ์

# เปิดไฟล์เสียงที่ต้องการอัปโหลด
with open(file_path, 'rb') as audio_file:
    files = {'file': audio_file}
    headers = {'Authorization': f'Bearer {api_key}'}  # การส่ง API key แบบ Bearer
    response = requests.post(url, files=files, headers=headers)

if response.status_code == 200:
    print("File uploaded successfully")
else:
    print("Failed to upload file:", response.text)