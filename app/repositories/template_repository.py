from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.template import Template
from app.repositories.base import BaseRepository


class TemplateRepository(BaseRepository[Template]):
    def __init__(self, session: AsyncSession):
        super().__init__(Template, session)

    async def get_by_email(self, email: str) -> Optional[Template]:
        return await super().get_by_email(email)

