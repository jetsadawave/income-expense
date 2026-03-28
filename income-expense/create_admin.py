"""
รันสคริปต์นี้เพื่อสร้าง Admin คนแรก
python create_admin.py
"""
from database import SessionLocal, engine, Base
from models import User
from passlib.context import CryptContext

# สร้าง table ถ้ายังไม่มี
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

email = "admin@example.com"
existing = db.query(User).filter(User.email == email).first()

if existing:
    print(f"Admin มีอยู่แล้ว: {email}")
else:
    admin = User(
        name="Admin",
        email=email,
        password=pwd_context.hash("admin1234"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    print("✅ สร้าง Admin สำเร็จ!")
    print(f"   Email: {email}")
    print(f"   Password: admin1234")

db.close()
