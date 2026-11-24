# Loung Work

Produto da Loung Tech para buscar vagas, preparar currículos com IA e acompanhar candidaturas. A Fase 0 entrega a página institucional e a infraestrutura de desenvolvimento e integração.

## Stack e equipes

- **Frontend · Mike (Miqueias) e Laís.** Next.js App Router, React, TypeScript strict, Tailwind CSS, shadcn/ui, React Hook Form e Zod.
- **Backend · Fernando e Marwin.** Python, FastAPI, Pydantic, SQLAlchemy 2, Alembic, pytest e Ruff.
- **Infraestrutura planejada.** Supabase Postgres, Auth e Storage privado, GitHub Actions, Vercel para web e serviço ASGI para API.

```text
apps/web/              Next.js, componentes e fundação da interface
apps/api/              FastAPI, schemas, Alembic e testes
packages/api-client/  Cliente HTTP tipado do contrato ativo
docs/                 Arquitetura, banco, API, setup e roadmap
infra/                Orientações para hospedagem futura
.github/              CI e template de PR
```

## Executar no Windows PowerShell

Use Node.js 24 com npm e Python 3.13. Na raiz:

```powershell
npm.cmd ci
Copy-Item apps/web/.env.example apps/web/.env.local
Copy-Item apps/api/.env.example apps/api/.env
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -c apps/api/constraints.txt -e './apps/api[dev]'
```

Em dois terminais na raiz:

```powershell
npm.cmd run dev
```

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --no-access-log
```

O frontend abre em `http://localhost:3000`. A API oferece `http://127.0.0.1:8000/health` e Swagger em `http://127.0.0.1:8000/docs`. A página e o health funcionam com as credenciais em branco.

Para rodar os testes, use `npm.cmd test` e `.\.venv\Scripts\python.exe -m pytest apps/api`. Consulte o [guia de desenvolvimento](docs/development-guide.md) para variáveis, macOS/Linux e validação completa. Para enviar mudanças, siga [CONTRIBUTING.md](CONTRIBUTING.md).
