# Ambiente de desenvolvimento

O [README](../README.md) contém os comandos PowerShell. Em macOS e Linux, use `npm` e `.venv/bin/python` no lugar de `npm.cmd` e `.\.venv\Scripts\python.exe`.

| Arquivo local       | Variável                             | Uso                                                      |
| ------------------- | ------------------------------------ | -------------------------------------------------------- |
| apps/web/.env.local | NEXT_PUBLIC_API_URL                  | Origem HTTP da API que o navegador pode acessar          |
| apps/web/.env.local | NEXT_PUBLIC_SUPABASE_URL             | URL do projeto Supabase                                  |
| apps/web/.env.local | NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY | Chave pública com prefixo sb_publishable_                |
| apps/api/.env       | APP_ENV                              | development, test ou production                          |
| apps/api/.env       | CORS_ORIGINS                         | Lista JSON das origens web permitidas                    |
| apps/api/.env       | DATABASE_URL                         | DSN no formato postgresql+psycopg:// com TLS no Supabase |
| apps/api/.env       | SUPABASE_URL                         | HTTPS do projeto que emite os JWTs                       |

Para integrar Auth, configure as URLs do mesmo projeto nas duas aplicações, a chave publicável no frontend e ative uma chave assimétrica ES256 ou RS256 no Supabase. Depois implemente os fluxos de sessão e use a dependência `current_user_id` nas rotas protegidas. Para conectar o banco, preencha o DSN conforme a conexão direta ou pooler de sessão do projeto e use credenciais distintas para migrations e para a API. Guarde credenciais de banco no backend.

```powershell
npm.cmd run format:check
npm.cmd run lint
npm.cmd run typecheck
npm.cmd test
npm.cmd run build
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m ruff check apps/api
.\.venv\Scripts\python.exe -m ruff format --check apps/api
.\.venv\Scripts\python.exe -m pytest apps/api
.\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini upgrade head --sql
```

Use `npm.cmd run format` e `.\.venv\Scripts\python.exe -m ruff format apps/api` para formatar. O build pode ser executado com `npm.cmd run start`. O lockfile npm e as constraints Python fixam o conjunto de dependências usado no setup e na CI.
