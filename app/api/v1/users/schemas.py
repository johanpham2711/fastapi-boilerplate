from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: str
    name: str | None = None

    class Config:
        from_attributes = True


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int

