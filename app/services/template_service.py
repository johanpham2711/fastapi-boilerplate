from typing import Any, Optional
from app.repositories.template_repository import TemplateRepository
from app.models.template import Template


class TemplateService:
    def __init__(self, template_repository: TemplateRepository):
        self.template_repository = template_repository

    async def create_template(self, template_data: dict[str, Any]) -> Template:
        return await self.template_repository.create(template_data)

    async def get_template_by_id(self, template_id: str) -> Optional[Template]:
        return await self.template_repository.get_by_id(template_id)

    async def get_template_by_email(self, email: str) -> Optional[Template]:
        return await self.template_repository.get_by_email(email)

    async def update_template(self, template_id: str, template_data: dict[str, Any]) -> Optional[Template]:
        return await self.template_repository.update(template_id, template_data)

    async def delete_template(self, template_id: str) -> bool:
        return await self.template_repository.delete(template_id)

    async def get_all_templates(self, skip: int = 0, limit: int = 100) -> list[Template]:
        return await self.template_repository.get_all(skip, limit)

