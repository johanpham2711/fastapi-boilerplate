from fastapi import APIRouter, Depends, HTTPException, status, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from secrets import token_urlsafe
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.api.v1.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    ForgotPasswordRequest,
    VerifyForgotPasswordRequest,
)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.cache_service import cache_service
from app.services.email_service import email_service
import uuid

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="API register new user")
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    existing_user = await user_repo.get_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_data = {
        "id": str(uuid.uuid4()),
        "email": request.email,
        "name": request.name,
        "password": get_password_hash(request.password),
    }

    user = await user_service.create_user(user_data)
    
    await email_service.send_welcome_email(request.email, user.name or "User")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
    )


@router.post("/login", response_model=TokenResponse, summary="API login")
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(request.email)

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


from fastapi import Request

@router.post("/logout", status_code=status.HTTP_200_OK, summary="API logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required",
        )
    await cache_service.set_blacklist_token(token, ttl=3600)
    return {"message": "Logged out successfully"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK, summary="API forgot password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(request.email)
    
    if not user:
        return {"message": "If that email exists, we'll send a password reset link."}
    
    reset_token = token_urlsafe(32)
    await cache_service.set(f"reset_token:{request.email}", reset_token, ttl=3600)
    
    await email_service.send_password_reset_email(request.email, reset_token)
    
    return {"message": "If that email exists, we'll send a password reset link."}


@router.post("/forgot-password/verify", status_code=status.HTTP_200_OK, summary="API verify forgot password")
async def verify_forgot_password(
    request: VerifyForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(request.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    stored_token = await cache_service.get(f"reset_token:{request.email}")
    
    if not stored_token or stored_token != request.reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    hashed_password = get_password_hash(request.new_password)
    await user_repo.update(user.id, {"password": hashed_password})
    
    await cache_service.delete(f"reset_token:{request.email}")
    
    return {"message": "Password reset successfully"}
