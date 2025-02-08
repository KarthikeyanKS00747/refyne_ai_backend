# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UploadResponse(BaseModel):
    file_id: str
    message: str

class UserDataBase(BaseModel):
    file_id: str
    original_filename: str
    string1: str
    string2: str
    processed: bool
    upload_date: datetime

    class Config:
        from_attributes = True

class UserDataDetail(UserDataBase):
    csv_data: str

class UserFilesList(BaseModel):
    files: List[UserDataBase]

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
