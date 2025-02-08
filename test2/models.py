# models.py
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Add relationship to UserData
    files = relationship("UserData", back_populates="user")

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_filename = Column(String)
    csv_data = Column(String)
    string1 = Column(String)
    string2 = Column(String)
    processed = Column(Boolean, default=False)
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Add relationship to User
    user = relationship("User", back_populates="files")