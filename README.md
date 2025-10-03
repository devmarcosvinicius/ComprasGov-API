# ComprasGov API

API RESTful com FastAPI, SQLAlchemy e SQLite. Autenticação JWT, paginação e ordenação. Dataset base: Compras Públicas (dados.gov.br). Esta entrega foca na estrutura estável com boas práticas.

---

## 👥 Alunos
- José Maria da Silva Junior
- Gabriel Aías Marques Mafra
- Lucas Juscelino
- Marcos Vinicius Viana Pavão
- Pedro Henrique Passos

---

## 📋 Requisitos
- Python 3.11+
- macOS/Linux/Windows
- Recomenda-se usar ambiente virtual (venv)

---

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd comprasgov-api
```

### 2. Crie e ative o ambiente virtual
**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

---

## ▶️ Execução

### 1. Inicie a API
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

### 2. Popule o banco de dados (seed)
Em outro terminal (com venv ativo):
```bash
python -m app.seed
```

### 3. Crie o usuário administrador
Acesse o Swagger UI em **http://localhost:8000/docs** e execute:
- `POST /users/seed-admin` → cria admin com credenciais:
  - **Email:** `admin@example.com`
  - **Senha:** `admin123`

### 4. Obtenha o token JWT
- `POST /users/token` → informe as credenciais acima
- Copie o `access_token` retornado
- No Swagger, clique em **"Authorize"** e cole o token no formato: `Bearer <seu_token>`

---

## 📚 Documentação

- **Swagger UI (interativo):** http://localhost:8000/docs
- **ReDoc (alternativo):** http://localhost:8000/redoc

---

## 🗂️ Estrutura do Projeto

```
comprasgov-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── database.py          # Configuração SQLAlchemy + SQLite
│   ├── models.py            # Modelos ORM (entidades)
│   ├── schemas.py           # Schemas Pydantic (validação)
│   ├── auth.py              # Autenticação JWT + bcrypt
│   ├── deps.py              # Dependências reutilizáveis
│   ├── utils.py             # Funções auxiliares (paginação, ordenação)
│   ├── seed.py              # Script de seed do banco
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py         # Endpoints de usuários
│   │   ├── orgaos.py        # Endpoints de órgãos
│   │   ├── fornecedores.py  # Endpoints de fornecedores
│   │   ├── licitacoes.py    # Endpoints de licitações
│   │   └── itens.py         # Endpoints de itens de licitação
│   └── services/
│       ├── __init__.py
│       ├── users_service.py
│       └── domain_service.py
├── data/
│   ├── seed_orgaos.csv
│   ├── seed_fornecedores.csv
│   ├── seed_licitacoes.csv
│   └── seed_itens.csv
├── tests/
│   └── postman_collection.json
├── requirements.txt
└── README.md
```

---

## 🔐 Autenticação e Autorização

A API utiliza **JWT (JSON Web Tokens)** para autenticação.

### Perfis de usuário:
- **admin:** pode criar, editar e deletar recursos
- **leitor:** pode apenas visualizar recursos

### Rotas protegidas:
- `POST /orgaos` → requer role `admin`
- `POST /fornecedores` → requer role `admin`
- `POST /licitacoes` → requer role `admin`
- `POST /itens` → requer role `admin`
- `DELETE /orgaos/{id}` → requer role `admin`

### Rotas públicas (ou com autenticação opcional):
- `GET /orgaos`, `GET /fornecedores`, `GET /licitacoes`, `GET /itens`

---

## 🎯 Funcionalidades Implementadas

### ✅ Entidades e Relacionamentos
- **Usuario** (autenticação)
- **Orgao** (órgãos compradores)
- **Fornecedor** (empresas fornecedoras)
- **Licitacao** (processos licitatórios)
- **ItemLicitacao** (itens/produtos de cada licitação)

### ✅ Relacionamentos:
- Orgao 1:N Licitacao
- Licitacao 1:N ItemLicitacao
- Fornecedor 1:N ItemLicitacao

### ✅ CRUD Completo
Todos os endpoints implementam operações de:
- **C**reate (POST)
- **R**ead (GET - lista e detalhes)
- **U**pdate (em desenvolvimento)
- **D**elete (DELETE)

### ✅ Paginação e Ordenação
Todos os endpoints de listagem aceitam:
- `page` (padrão: 1)
- `size` (padrão: 20, máx: 100)
- `order_by` (nome do campo)
- `direction` (asc | desc)

**Exemplo:**
```
GET /orgaos?page=1&size=10&order_by=nome&direction=asc
```

### ✅ Filtros Dinâmicos
- **Licitações:** `orgao_id`, `ano`
- **Itens:** `licitacao_id`, `fornecedor_id`

**Exemplo:**
```
GET /licitacoes?orgao_id=2&ano=2024
GET /itens?licitacao_id=1&fornecedor_id=3
```

---

## 🧪 Testes

### Postman Collection
Importe o arquivo `tests/postman_collection.json` no Postman.

**Variáveis de ambiente:**
- `base_url`: `http://localhost:8000`
- `token`: (será preenchido automaticamente após login)

**Fluxo de testes:**
1. Health Check
2. Seed Admin
3. Login (gera token automaticamente)
4. Listar Órgãos
5. Criar Órgão (admin)
6. Listar Fornecedores
7. Criar Fornecedor (admin)
8. Listar Licitações
9. Criar Licitação (admin)
10. Listar Itens

---

## 📊 Modelagem de Dados

### Diagrama ER (resumo)
![Texto Alternativo](/modelo-er.png "Modelo ER")
```
Usuario
  ├── id (PK)
  ├── email (unique)
  ├── hash_senha
  └── role (admin | leitor)

Orgao
  ├── id (PK)
  ├── nome
  ├── uf
  └── licitacoes (1:N)

Fornecedor
  ├── id (PK)
  ├── nome
  ├── cnpj (unique)
  └── itens (1:N)

Licitacao
  ├── id (PK)
  ├── numero
  ├── ano
  ├── orgao_id (FK)
  └── itens (1:N)

ItemLicitacao
  ├── id (PK)
  ├── licitacao_id (FK)
  ├── fornecedor_id (FK)
  ├── descricao_item
  ├── quantidade
  └── valor_unitario
```

---

## 📦 Dataset

### Origem
Portal dados.gov.br — Compras Públicas (Painel de Preços/Compras Governamentais)

### Formato
CSV/JSON (API e dumps públicos)

### Periodicidade
Atualização recorrente (tipicamente mensal ou mais frequente)

### Recorte para este projeto
Modelamos Órgãos (compradores), Fornecedores, Licitações e Itens da Licitação, cobrindo relacionamentos 1:N e N:N (via itens).

Para a primeira entrega, usamos um seed local (CSV simples) que representa um subconjunto coerente do dataset público, mantendo aderência ao escopo.

---

## 🔧 Tecnologias Utilizadas

- FastAPI 0.115.2 — Framework web moderno e rápido
- SQLAlchemy 2.0.35 — ORM para Python
- SQLite — Banco de dados relacional leve
- Pydantic 2.9.2 — Validação de dados
- Passlib + Bcrypt — Hash seguro de senhas
- Python-Jose — Geração e validação de JWT
- Uvicorn — Servidor ASGI de alta performance

---

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido como Entrega 1 da disciplina de Desenvolvimento de APIs RESTful, com foco em:

- Escolha e análise de conjunto de dados públicos
- Modelagem de dados com no mínimo 3 entidades relacionadas
- Implementação de banco de dados com SQLite
- Criação de API RESTful com FastAPI
- Autenticação JWT e controle de acesso
- Documentação automática (Swagger/OpenAPI)
- Testes manuais com Postman
- Versionamento com Git/GitHub

---

## 📝 Próximos Passos (Entregas Futuras)

- [ ] Implementar endpoints de UPDATE (PUT/PATCH)
- [ ] Adicionar testes automatizados (pytest)
- [ ] Migrar para PostgreSQL
- [ ] Implementar cache com Redis
- [ ] Adicionar logs estruturados
- [ ] Deploy em cloud (Heroku/Railway/AWS)
- [ ] Implementar CI/CD com GitHub Actions
- [ ] Adicionar rate limiting
- [ ] Implementar busca full-text
- [ ] Criar dashboard de visualização de dados

---

## 📄 Licença

Este projeto é de uso acadêmico e está disponível sob a licença MIT.

---

## 📞 Contato

Para dúvidas ou sugestões, entre em contato com a equipe através do repositório do projeto.

---

**Desenvolvido com ❤️ pela equipe ComprasGov**
