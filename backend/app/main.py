from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import database, models, utils, auth, schemas

app = FastAPI()

@app.get("/")
def root():
    db = SessionLocal()
    try:
        db.execute("SELECT 1")
        return {"message": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"user_id": user.id, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user