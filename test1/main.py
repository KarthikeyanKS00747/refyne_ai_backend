#from enum import Enum
from fastapi import FastAPI, status, Depends, HTTPException
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
#from pydantic import BaseModel, EmailStr


# class User(BaseModel):
#     id: int
#     username: str
#     password: str
#     email: EmailStr
    

# items = {
#     0: User(id = 1, username = "aaa", password = "pass1", email = "abc@gmail.com"),
# # }
# app = FastAPI()
# @app.get("/")
# def index() -> dict[str, dict[int, User]]:
#     return {"ites": items}