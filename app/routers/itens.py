from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth
from ..utils import apply_pagination, apply_ordering
from ..deps import pagination_params

router = APIRouter(prefix="/itens", tags=["Itens de Licitação"])

@router.post("/", response_model=schemas.ItemOut, dependencies=[Depends(auth.require_role("admin"))])
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    if not db.query(models.Licitacao).get(payload.licitacao_id):
        raise HTTPException(status_code=400, detail="Licitação inválida")
    if not db.query(models.Fornecedor).get(payload.fornecedor_id):
        raise HTTPException(status_code=400, detail="Fornecedor inválido")
    it = models.ItemLicitacao(**payload.model_dump())
    db.add(it); db.commit(); db.refresh(it)
    return it

@router.get("/", response_model=list[schemas.ItemOut])
def list_itens(
    db: Session = Depends(get_db),
    page_size: dict = Depends(pagination_params),
    order_by: str | None = Query(None),
    direction: str = Query("asc", pattern="^(asc|desc)$"),
    licitacao_id: int | None = None,
    fornecedor_id: int | None = None,
):
    q = db.query(models.ItemLicitacao)
    if licitacao_id:
        q = q.filter(models.ItemLicitacao.licitacao_id == licitacao_id)
    if fornecedor_id:
        q = q.filter(models.ItemLicitacao.fornecedor_id == fornecedor_id)
    q = apply_ordering(q, models.ItemLicitacao, order_by, direction)
    total, items = apply_pagination(q, page=page_size["page"], size=page_size["size"])
    return items