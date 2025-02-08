from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt
from database import SessionLocal
from models import User

app = FastAPI()

# Utility function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}
