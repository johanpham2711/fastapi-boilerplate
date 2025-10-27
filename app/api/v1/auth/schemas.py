from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyForgotPasswordRequest(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str | None = None

    class Config:
        from_attributes = True
