from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth
from ..utils import apply_pagination, apply_ordering
from ..deps import pagination_params

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])

@router.post("/", response_model=schemas.FornecedorOut, dependencies=[Depends(auth.require_role("admin"))])
def create_fornecedor(payload: schemas.FornecedorCreate, db: Session = Depends(get_db)):
    if db.query(models.Fornecedor).filter(models.Fornecedor.cnpj == payload.cnpj).first():
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    f = models.Fornecedor(nome=payload.nome, cnpj=payload.cnpj)
    db.add(f); db.commit(); db.refresh(f)
    return f

@router.get("/", response_model=list[schemas.FornecedorOut])
def list_fornecedores(
    db: Session = Depends(get_db),
    page_size: dict = Depends(pagination_params),
    order_by: str | None = Query(None),
    direction: str = Query("asc", pattern="^(asc|desc)$"),
):
    q = db.query(models.Fornecedor)
    q = apply_ordering(q, models.Fornecedor, order_by, direction)
    total, items = apply_pagination(q, page=page_size["page"], size=page_size["size"])
    return items

@router.get("/{fornecedor_id}", response_model=schemas.FornecedorOut)
def get_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    f = db.query(models.Fornecedor).get(fornecedor_id)
    if not f:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return f