from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth
from ..utils import apply_pagination, apply_ordering
from ..deps import pagination_params

router = APIRouter(prefix="/orgaos", tags=["Órgãos"])

@router.post("/", response_model=schemas.OrgaoOut, dependencies=[Depends(auth.require_role("admin"))])
def create_orgao(payload: schemas.OrgaoCreate, db: Session = Depends(get_db)):
    org = models.Orgao(nome=payload.nome, uf=payload.uf.upper())
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.get("/", response_model=list[schemas.OrgaoOut])
def list_orgaos(
    db: Session = Depends(get_db),
    page_size: dict = Depends(pagination_params),
    order_by: str | None = Query(None),
    direction: str = Query("asc", pattern="^(asc|desc)$"),
):
    q = db.query(models.Orgao)
    q = apply_ordering(q, models.Orgao, order_by, direction)
    total, items = apply_pagination(q, page=page_size["page"], size=page_size["size"])
    return items

@router.get("/{orgao_id}", response_model=schemas.OrgaoOut)
def get_orgao(orgao_id: int, db: Session = Depends(get_db)):
    org = db.query(models.Orgao).get(orgao_id)
    if not org:
        raise HTTPException(status_code=404, detail="Órgão não encontrado")
    return org

@router.delete("/{orgao_id}", dependencies=[Depends(auth.require_role("admin"))])
def delete_orgao(orgao_id: int, db: Session = Depends(get_db)):
    org = db.query(models.Orgao).get(orgao_id)
    if not org:
        raise HTTPException(status_code=404, detail="Órgão não encontrado")
    db.delete(org)
    db.commit()
    return {"ok": True}