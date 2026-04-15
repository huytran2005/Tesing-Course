from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from models.user import User
from schemas.auth_schema import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
    StaffCreateRequest,
)
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from utils.dependencies import get_current_user
from controllers.restaurant_controller import _create_staff_account

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    # determine role from request if provided; default to 'customer'
    role = getattr(data, "role", "customer")
    if role not in ("customer", "owner", "staff"):
        role = "customer"

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        display_name=data.display_name,
        phone=data.phone,
        role=role,
    )

    db.add(user)
    db.commit()

    return {"message": "Register successful"}


@router.post("/staff", response_model=RegisterResponse, status_code=201)
@router.post("/staff-account", response_model=RegisterResponse, status_code=201)
def create_staff_account(
    data: StaffCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return _create_staff_account(
        restaurant_id=data.restaurant_id,
        data=RegisterRequest(
            email=data.email,
            password=data.password,
            display_name=data.display_name,
            phone=data.phone,
        ),
        db=db,
        current_user=current_user,
    )


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # staff = thiết bị quán → BẮT BUỘC có restaurant_id
    if user.role == "staff" and not user.restaurant_id:
        raise HTTPException(
            status_code=403,
            detail="Staff account is not bound to any restaurant",
        )

    token = create_access_token({
        "user_id": str(user.id),
        "role": user.role,
        "restaurant_id": str(user.restaurant_id) if user.restaurant_id else None,
    })

    return {"access_token": token}
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "restaurant_id": (
            str(current_user.restaurant_id)
            if current_user.restaurant_id
            else None
        ),
    }
