from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

class UserBase(BaseModel):
    manager_id: str = Field(..., max_length=255)
    name: str = Field(..., max_length=255)
    organization_name: str = Field(..., max_length=255)
    email: EmailStr = Field(...)
    class Config:
        orm_mode = True
    
class UserCreate(UserBase):
    password: str = Field(...)
    @validator('manager_id')
    def manager_id_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Manager ID must not be empty")
        if len(v) > 255:
            raise ValueError("Manager ID must be less than 255 characters long")
        return v
    
    @validator('password')
    def password_length(cls, v) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('email')
    def email_length(cls, v) -> str:
        if len(v) > 255:
            raise ValueError('Email must be less than 255 characters long')
        return v

    @validator('name')
    def username_length(cls, v) -> str:
        if len(v) > 255:
            raise ValueError('Username must be less than 255 characters long')
        return v

    @validator('organization_name')
    def organization_name_length(cls, v) -> str:
        if len(v) > 255:
            raise ValueError(
                'Company name must be less than 255 characters long')
        return v

    @validator('email')
    def email_lowercase(cls, v) -> str:
        return v.lower()
    
class User(UserBase):
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime = None

    class Config:
        orm_mode = True
