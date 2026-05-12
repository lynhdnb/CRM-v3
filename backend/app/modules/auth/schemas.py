"""Pydantic schemas for Authentication"""
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """Схема для запроса входа"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Схема для ответа с токеном"""
    access_token: str
    token_type: str = "bearer"