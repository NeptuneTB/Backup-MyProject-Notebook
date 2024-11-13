import secrets

# สร้าง SECRET_KEY และ JWT_SECRET_KEY
SECRET_KEY = secrets.token_hex(16)  # คีย์ 32 อักขระ (16 ไบต์)
JWT_SECRET_KEY = secrets.token_hex(16)  # คีย์ 32 อักขระ (16 ไบต์)

print("SECRET_KEY:", SECRET_KEY)
print("JWT_SECRET_KEY:", JWT_SECRET_KEY)
