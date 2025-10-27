from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.user import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: dict[str, Any]) -> User:
        return await self.user_repository.create(user_data)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)

    async def update_user(self, user_id: str, user_data: dict[str, Any]) -> Optional[User]:
        return await self.user_repository.update(user_id, user_data)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repository.get_all(skip, limit)

