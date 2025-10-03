from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hash_senha: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="leitor")  # admin | leitor

class Orgao(Base):
    __tablename__ = "orgaos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True, nullable=False)
    uf: Mapped[str] = mapped_column(String(2), index=True, nullable=False)
    licitacoes: Mapped[list["Licitacao"]] = relationship("Licitacao", back_populates="orgao")

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True, nullable=False)
    cnpj: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    itens: Mapped[list["ItemLicitacao"]] = relationship("ItemLicitacao", back_populates="fornecedor")

class Licitacao(Base):
    __tablename__ = "licitacoes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero: Mapped[str] = mapped_column(String, index=True, nullable=False)
    ano: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    orgao_id: Mapped[int] = mapped_column(ForeignKey("orgaos.id"), index=True)
    orgao: Mapped["Orgao"] = relationship("Orgao", back_populates="licitacoes")
    itens: Mapped[list["ItemLicitacao"]] = relationship("ItemLicitacao", back_populates="licitacao", cascade="all, delete-orphan")

class ItemLicitacao(Base):
    __tablename__ = "itens_licitacao"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    licitacao_id: Mapped[int] = mapped_column(ForeignKey("licitacoes.id"), index=True)
    fornecedor_id: Mapped[int] = mapped_column(ForeignKey("fornecedores.id"), index=True)
    descricao_item: Mapped[str] = mapped_column(String, index=True, nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    licitacao: Mapped["Licitacao"] = relationship("Licitacao", back_populates="itens")
    fornecedor: Mapped["Fornecedor"] = relationship("Fornecedor", back_populates="itens")