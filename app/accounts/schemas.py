from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class BaseUserSchema(BaseModel):
    id: Optional[UUID] = Field(None)
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class UserSchema(BaseUserSchema):
    password: str | None = None


class UserResponseSchema(BaseUserSchema):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserRegistrationForm(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr = Field(description="Email address")
    password: str = Field(min_length=8, max_length=64)


class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
