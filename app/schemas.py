from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str
    role: str

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str
    role: str = "leitor"

class UsuarioOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    class Config:
        from_attributes = True

# Domain
class OrgaoBase(BaseModel):
    nome: str
    uf: str = Field(min_length=2, max_length=2)

class OrgaoCreate(OrgaoBase): ...
class OrgaoOut(OrgaoBase):
    id: int
    class Config:
        from_attributes = True

class FornecedorBase(BaseModel):
    nome: str
    cnpj: str

class FornecedorCreate(FornecedorBase): ...
class FornecedorOut(FornecedorBase):
    id: int
    class Config:
        from_attributes = True

class LicitacaoBase(BaseModel):
    numero: str
    ano: int
    orgao_id: int

class LicitacaoCreate(LicitacaoBase): ...
class LicitacaoOut(LicitacaoBase):
    id: int
    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    licitacao_id: int
    fornecedor_id: int
    descricao_item: str
    quantidade: int
    valor_unitario: float

class ItemCreate(ItemBase): ...
class ItemOut(ItemBase):
    id: int
    class Config:
        from_attributes = True

# Commons
class PageMeta(BaseModel):
    total: int
    page: int
    size: int

class PageResponse(BaseModel):
    meta: PageMeta
    data: list