import csv
from pathlib import Path
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Orgao, Fornecedor, Licitacao, ItemLicitacao

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def seed(db: Session):
    if db.query(Orgao).first():
        print("Seed já aplicado.")
        return

    # Orgaos
    with open(DATA_DIR / "seed_orgaos.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Orgao(nome=row["nome"], uf=row["uf"]))
    db.commit()

    # Fornecedores
    with open(DATA_DIR / "seed_fornecedores.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Fornecedor(nome=row["nome"], cnpj=row["cnpj"]))
    db.commit()

    # Licitações
    with open(DATA_DIR / "seed_licitacoes.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(Licitacao(numero=row["numero"], ano=int(row["ano"]), orgao_id=int(row["orgao_id"])))
    db.commit()

    # Itens
    with open(DATA_DIR / "seed_itens.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            db.add(ItemLicitacao(
                licitacao_id=int(row["licitacao_id"]),
                fornecedor_id=int(row["fornecedor_id"]),
                descricao_item=row["descricao_item"],
                quantidade=int(row["quantidade"]),
                valor_unitario=float(row["valor_unitario"])
            ))
    db.commit()
    print("Seed concluído.")

if __name__ == "__main__":
    db = SessionLocal()
    seed(db)
    db.close()