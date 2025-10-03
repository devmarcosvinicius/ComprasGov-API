from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import users, orgaos, fornecedores, licitacoes, itens

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Compras Públicas - Entrega 1",
    version="1.0.0",
    description="API RESTful com FastAPI, SQLAlchemy e SQLite. Autenticação JWT, paginação e ordenação."
)

# Agrupar rotas
app.include_router(users.router)
app.include_router(orgaos.router)
app.include_router(fornecedores.router)
app.include_router(licitacoes.router)
app.include_router(itens.router)

@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}