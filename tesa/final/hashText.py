import hashlib

def generate_secret_key_from_text(text):
    # แปลงข้อความให้เป็น bytes แล้วใช้ hashlib.sha256() เพื่อแฮช
    text_bytes = text.encode('utf-8')
    sha256_hash = hashlib.sha256(text_bytes)
    # ส่งคืนค่าแฮชในรูปแบบ hexadecimal
    secret_key = sha256_hash.hexdigest()
    return secret_key

# ตัวอย่างการใช้งาน
text = "list-data"
secret_key = generate_secret_key_from_text(text)

print("Secret Key:", secret_key)
