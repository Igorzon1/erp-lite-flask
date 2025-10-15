# 🧠 ERP Lite Flask — Sistema de Gerenciamento de Estoque, Pedidos e Clientes

## 📋 Resumo
Sistema web completo de gerenciamento de **clientes**, **produtos/estoque** e **pedidos**, desenvolvido com **Flask (Python)** no padrão **MVC**.  
O projeto foi criado como portfólio colaborativo entre um estudante de **Ciência da Computação** (backend) e um **Engenheiro de Produção** (regras operacionais e logísticas), com foco em **boas práticas**, **arquitetura organizada** e **aplicação de conceitos reais de gestão de estoque**.

---

## 🚀 Tecnologias

- **Linguagem:** Python 3.12+
- **Framework:** Flask  
- **Banco de Dados:** SQLite (dev) / PostgreSQL (produção)
- **ORM / Migrações:** SQLAlchemy + Alembic
- **Autenticação:** Flask-Login + JWT + Bcrypt
- **Frontend:** Bootstrap 5 + HTML + jQuery
- **Testes:** Pytest
- **Documentação da API:** Swagger (Flasgger)
- **Containerização:** Docker + Docker Compose

---

## 🎯 Objetivos do Projeto

O foco deste sistema é demonstrar:

- Estrutura organizada seguindo o padrão **MVC (Model-View-Controller)**  
- Autenticação moderna com **JWT** e **Flask-Login**  
- CRUDs modulares e desacoplados usando **Blueprints**  
- Integração de conceitos reais de estoque (**ABC**, **PEPS**, **endereçamento físico**)  
- Código limpo, legível e fácil de manter  
- Práticas de engenharia de produção aplicadas na modelagem de estoque e pedidos  

---

## ⚙️ Estrutura do Projeto

---

## Estrutura do repositório
```
erp-lite-flask/
│
├── app/
│ ├── controllers/ # Controladores (lógica de rotas e fluxo da aplicação)
│ │ ├── auth_controller.py
│ │ └── product_controller.py
│ │
│ ├── models/ # Modelos (tabelas e regras de negócio)
│ │ ├── user.py
│ │ └── product.py
│ │
│ ├── templates/ # Views (HTML com Bootstrap)
│ │ ├── auth/
│ │ ├── pedidos/
│ │ ├── products/
│ │ ├── layout.html
│ │ └── 404.html
│ │
│ ├── config.py # Configurações gerais do projeto
│ ├── extensions.py # Inicialização das extensões (DB, LoginManager, JWT, Bcrypt, Migrate)
│ └── init.py # Fábrica da aplicação Flask (create_app)
│
├── migrations/ # Migrações do Alembic
│
├── run.py # Ponto de entrada principal
├── requirements.txt # Dependências do projeto
├── .env # Variáveis de ambiente
├── .gitignore
└── README.md
```

---

## Modelagem (visão geral)
- **Client**: id, nome, cpf_cnpj, email, phone, endereço
- **Product**: id, sku, nome, descrição, peso, dimensões, classe_abc, perecível(boolean)
- **StockLocation**: id, corredor, prateleira, nível, capacidade (peso/volume)
- **InventoryBatch**: id, product_id, lote, data_validade, quantidade
- **InventoryMovement**: id, batch_id, tipo (entrada/saida/reserva), quantidade, documento (pedido_id)
- **Order**: id, client_id, status, total, created_at
- **OrderItem**: id, order_id, product_id, quantidade, unit_price, batch_allocated

## Diagrama de Classes no docs

---

## Scripts úteis / comandos
### Setup local (com Docker)
```bash
# build e start
docker-compose up --build -d

# rodar migrations
docker-compose exec web alembic upgrade head

# criar dados de amostra
docker-compose exec web python manage.py seed_data
```

### Setup sem Docker (ambiente dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# ajustar vars de DB
flask db upgrade
flask run --host 0.0.0.0 --port 8000
```

---

## Variáveis de ambiente (exemplo `.env.example`)
```
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=trocar_para_uma_chave_segura
DATABASE_URL=sqlite:///dev.db  # ou postgres://user:pass@host:port/dbname
JWT_SECRET=trocar_para_uma_chave_jwt
```

---

## Testes e qualidade
- Executar testes: `pytest --maxfail=1 --disable-warnings -q`
- Cobertura mínima alvo: **70%** (meta do projeto)
- Ferramentas sugeridas: `flake8`, `isort`, `black` (formatação), `pre-commit` hooks

---

## Endpoints principais (exemplos)
- `POST /auth/login` → autenticação (JWT)
- `POST /clients` → criar cliente
- `GET /clients/{id}` → obter cliente
- `POST /products` → criar produto
- `POST /inventory/entries` → registrar entrada de estoque (lote)
- `POST /orders` → criar pedido (reserva e cálculo)
- `PATCH /orders/{id}/confirm` → confirmar pedido (debita estoque)
- `PATCH /orders/{id}/cancel` → cancelar pedido (reverte movimentações)
- `GET /reports/movements` → relatórios de movimentação
- `GET /reports/occupancy` → ocupação por corredor/prateleira

---

## Como apresentar este projeto em entrevistas (dica para recrutadores)
- Explique a **separação de responsabilidades** (models, repositories, services) e por que isso facilita manutenção e testes.
- Mostre os **testes que cobrem regras de negócio** mais complexas (ex.: alocação PEPS, cancelamento de pedido que reverte estoque).
- Demonstre a **colaboração com o Engenheiro de Produção**: como os requisitos de logística (endereçamento, capacidade, políticas ABC/PEPS) influenciaram as decisões de modelagem e UI.
- Aponte o uso de **conteinerização** e como isso facilita replicar o ambiente do avaliador.

---

## O que cada membro da dupla entregou (para README do portfólio)
- **Estudante de Ciência da Computação (Desenvolvedor Backend):** arquitetura do backend, implementação de endpoints REST, autenticação JWT, testes automatizados, Docker, integração com Alembic/SQLAlchemy e documentação da API.
- **Engenheiro de Produção:** definição das regras de domínio de estoque (endereçamento, ABC, PEPS), métricas de ocupação e recomendações operacionais, checklists de qualidade e fluxos de inventário cíclico.

---

## Próximos passos / melhorias planejadas
- Integração com gateways de pagamento e emissão de NF-e.
- Dashboard analítico e exportação de relatórios (CSV / XLSX).
- Implementar filas (RabbitMQ / Celery) para processamento assíncrono de tarefas (ex.: geração de relatórios, notificações de vencimento).
- Monitoramento e CI/CD (ex.: GitHub Actions → deploy automático em staging).

---

## Como contribuir
1. Fork no repositório
2. Criar branch `feature/<nome>`
3. Abrir PR descrevendo mudanças e test coverage
4. Código deve seguir `black` + `flake8`

---

## Contato
- **Desenvolvedor (Ciência da Computação):** `igorzon` (GitHub) — *link no perfil do repositório*
- **Engenheiro de Produção:** `nome_do_amigo` — *incluir LinkedIn ou contato profissional*

---

## Licença
Projeto sob licença MIT.
Sinta-se à vontade para usar como base no seu portfólio. 🚀

---


