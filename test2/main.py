# main.py
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import auth
import models
import schemas
from database import engine, get_db
from config import settings
import pandas as pd
from typing import Annotated
import io
import uuid

from ml import refine, utils



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(auth.get_current_user)]
):
    return current_user

@app.post("/upload", response_model=schemas.UploadResponse)
async def upload(
    string1: Annotated[str, Form()],
    string2: Annotated[str, Form()],
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Read and validate CSV content
    contents = await file.read()
    csv_text = contents.decode('utf-8')
    
    try:
        # Validate CSV format
        df = pd.read_csv(io.StringIO(csv_text))
        utils.find_dataset(data_desc=string2, model_name=string1)

        # Basic validation
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    

    
    # Create database record
    db_data = models.UserData(
        user_id=current_user.id,
        file_id=file_id,
        original_filename=file.filename,
        csv_data=csv_text,
        string1=string1,
        string2=string2
    )
    
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    # utils.find_dataset(string2, string1)


    
    return {"file_id": file_id, "message": "File uploaded successfully"}

@app.get("/files", response_model=schemas.UserFilesList)
async def list_files(
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Session = Depends(get_db)
):
    files = db.query(models.UserData).filter(
        models.UserData.user_id == current_user.id
    ).order_by(models.UserData.upload_date.desc()).all()
    
    return {"files": files}

@app.get("/files/{file_id}", response_model=schemas.UserDataDetail)
async def get_file(
    file_id: str,
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Session = Depends(get_db)
):
    file = db.query(models.UserData).filter(
        models.UserData.file_id == file_id,
        models.UserData.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return file

@app.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Session = Depends(get_db)
):
    file = db.query(models.UserData).filter(
        models.UserData.file_id == file_id,
        models.UserData.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    db.delete(file)
    db.commit()
    
    return {"message": "File deleted successfully"}