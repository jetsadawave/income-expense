from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Transaction
from schemas import UserResponse, TransactionResponse
from auth import verify_token

router = APIRouter(prefix="/admin", tags=["Admin"])

# ฟังก์ชันตรวจสอบว่าเป็น admin
def get_admin_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ไม่ถูกต้อง")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="ไม่พบผู้ใช้งาน")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="คุณไม่มีสิทธิ์เข้าถึง Admin")
    return user

# ดู user ทั้งหมด
@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return db.query(User).all()

# ลบ user
@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ไม่พบ User นี้")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="ไม่สามารถลบ Admin ได้")
    db.delete(user)
    db.commit()

# ดู transaction ทั้งหมด
@router.get("/transactions", response_model=List[TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return db.query(Transaction).all()

# ลบ transaction
@router.delete("/transactions/{tx_id}", status_code=204)
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="ไม่พบรายการนี้")
    db.delete(tx)
    db.commit()

# เพิ่ม admin (สร้าง admin user ใหม่)
@router.post("/create-admin", response_model=UserResponse, status_code=201)
def create_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ไม่พบ User นี้")
    user.role = "admin"
    db.commit()
    db.refresh(user)
    return user
