from sqlalchemy.orm import Session
from .. import models

def exists_by_id(db: Session, model, id_: int) -> bool:
    return db.query(model).filter(model.id == id_).first() is not None