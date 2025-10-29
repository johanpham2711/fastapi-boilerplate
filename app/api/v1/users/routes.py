from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.security import get_password_hash
from app.api.v1.users.schemas import (
    UserResponse,
    UserCreateRequest,
    UserUpdateRequest,
    UserListResponse,
)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
import uuid

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create user")
async def create_user(
    request: UserCreateRequest,
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
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
    )


@router.get("/", response_model=UserListResponse, summary="Get all users")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    users = await user_service.get_all_users(skip, limit)
    return UserListResponse(
        users=[UserResponse(id=u.id, email=u.email, name=u.name) for u in users],
        total=len(users),
    )


@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
    )


@router.put("/{user_id}", response_model=UserResponse, summary="Update user")
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = request.model_dump(exclude_unset=True)
    updated_user = await user_service.update_user(user_id, update_data)

    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        name=updated_user.name,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await user_service.delete_user(user_id)
    return None

