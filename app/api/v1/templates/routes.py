from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_password_hash
from app.api.v1.templates.schemas import (
    TemplateResponse,
    TemplateCreateRequest,
    TemplateUpdateRequest,
    TemplateListResponse,
)
from app.repositories.template_repository import TemplateRepository
from app.services.template_service import TemplateService
import uuid

router = APIRouter()


@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    request: TemplateCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    template_repo = TemplateRepository(db)
    template_service = TemplateService(template_repo)

    existing_template = await template_repo.get_by_email(request.email)
    if existing_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    template_data = {
        "id": str(uuid.uuid4()),
        "email": request.email,
        "name": request.name,
        "password": get_password_hash(request.password),
        "published": request.published,
    }

    template = await template_service.create_template(template_data)
    return TemplateResponse(
        id=template.id,
        email=template.email,
        name=template.name,
        published=template.published,
    )


@router.get("/", response_model=TemplateListResponse)
async def get_templates(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    template_repo = TemplateRepository(db)
    template_service = TemplateService(template_repo)

    templates = await template_service.get_all_templates(skip, limit)
    return TemplateListResponse(
        templates=[
            TemplateResponse(id=t.id, email=t.email, name=t.name, published=t.published)
            for t in templates
        ],
        total=len(templates),
    )


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
):
    template_repo = TemplateRepository(db)
    template_service = TemplateService(template_repo)

    template = await template_service.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    return TemplateResponse(
        id=template.id,
        email=template.email,
        name=template.name,
        published=template.published,
    )


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    request: TemplateUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    template_repo = TemplateRepository(db)
    template_service = TemplateService(template_repo)

    template = await template_service.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    update_data = request.model_dump(exclude_unset=True)
    updated_template = await template_service.update_template(template_id, update_data)

    return TemplateResponse(
        id=updated_template.id,
        email=updated_template.email,
        name=updated_template.name,
        published=updated_template.published,
    )


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
):
    template_repo = TemplateRepository(db)
    template_service = TemplateService(template_repo)

    template = await template_service.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    await template_service.delete_template(template_id)
    return None

