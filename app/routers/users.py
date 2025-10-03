from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from .. import schemas, models, auth
from ..services.users_service import create_user

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("/", response_model=schemas.UsuarioOut)
def create_user_endpoint(payload: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter(models.Usuario.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = create_user(db, payload.email, payload.senha, payload.role)
    return user

@router.post("/seed-admin", response_model=schemas.UsuarioOut)
def seed_admin(db: Session = Depends(get_db)):
    email = "admin@example.com"
    if db.query(models.Usuario).filter(models.Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="Admin já existe")
    return create_user(db, email, "admin123", "admin")

@router.post("/token", tags=["Auth"], response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = auth.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}