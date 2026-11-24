# Hospedagem futura

Configure Vercel para `apps/web` com acesso ao workspace npm da raiz. Para a API, use um serviço compatível com ASGI e execute `uvicorn app.main:app --host 0.0.0.0 --port <porta> --no-access-log` com `/health` como verificação do processo. Configure as origens do frontend no backend, as variáveis públicas na Vercel e os segredos no serviço da API. Execute migrations em uma etapa separada usando o papel de migração.
