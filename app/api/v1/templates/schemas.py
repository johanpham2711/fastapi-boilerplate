from pydantic import BaseModel, EmailStr


class TemplateResponse(BaseModel):
    id: str
    email: str
    name: str | None = None
    published: bool = False

    class Config:
        from_attributes = True


class TemplateCreateRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None
    published: bool = False


class TemplateUpdateRequest(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    published: bool | None = None


class TemplateListResponse(BaseModel):
    templates: list[TemplateResponse]
    total: int

