from enum import StrEnum
from pydantic import BaseModel, EmailStr

class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


class UserPublic(BaseModel):
    """Публичная схема пользователя (без пароля и хеша)."""
    id: int
    email: EmailStr
    role: UserRole 

    model_config = {"from_attributes": True}