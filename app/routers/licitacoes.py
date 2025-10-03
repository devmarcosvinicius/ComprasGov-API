from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth
from ..utils import apply_pagination, apply_ordering
from ..deps import pagination_params

router = APIRouter(prefix="/licitacoes", tags=["Licitações"])

@router.post("/", response_model=schemas.LicitacaoOut, dependencies=[Depends(auth.require_role("admin"))])
def create_licitacao(payload: schemas.LicitacaoCreate, db: Session = Depends(get_db)):
    if not db.query(models.Orgao).get(payload.orgao_id):
        raise HTTPException(status_code=400, detail="Órgão inválido")
    lic = models.Licitacao(numero=payload.numero, ano=payload.ano, orgao_id=payload.orgao_id)
    db.add(lic); db.commit(); db.refresh(lic)
    return lic

@router.get("/", response_model=list[schemas.LicitacaoOut])
def list_licitacoes(
    db: Session = Depends(get_db),
    page_size: dict = Depends(pagination_params),
    order_by: str | None = Query(None),
    direction: str = Query("asc", pattern="^(asc|desc)$"),
    orgao_id: int | None = None,
    ano: int | None = None,
):
    q = db.query(models.Licitacao)
    if orgao_id:
        q = q.filter(models.Licitacao.orgao_id == orgao_id)
    if ano:
        q = q.filter(models.Licitacao.ano == ano)
    q = apply_ordering(q, models.Licitacao, order_by, direction)
    total, items = apply_pagination(q, page=page_size["page"], size=page_size["size"])
    return items

@router.get("/{licitacao_id}", response_model=schemas.LicitacaoOut)
def get_licitacao(licitacao_id: int, db: Session = Depends(get_db)):
    lic = db.query(models.Licitacao).get(licitacao_id)
    if not lic:
        raise HTTPException(status_code=404, detail="Licitação não encontrada")
    return lic