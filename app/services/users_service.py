from sqlalchemy.orm import Session
from .. import models, auth

def create_user(db: Session, email: str, senha: str, role: str = "leitor"):
    user = models.Usuario(email=email, hash_senha=auth.get_password_hash(senha), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user