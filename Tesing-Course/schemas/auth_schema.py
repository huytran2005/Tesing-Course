from pydantic import BaseModel, EmailStr
from uuid import UUID


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None
    phone: str | None = None


class RegisterResponse(BaseModel):
    message: str


class StaffCreateRequest(BaseModel):
    restaurant_id: UUID
    email: EmailStr
    password: str
    display_name: str | None = None
    phone: str | None = None


class StaffResponse(BaseModel):
    id: UUID
    restaurant_id: UUID | None = None
    email: EmailStr
    display_name: str | None = None
    phone: str | None = None
    role: str

    model_config = {
        "from_attributes": True,
    }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
