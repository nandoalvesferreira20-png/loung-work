# Contrato HTTP

O OpenAPI servido em `/openapi.json` é a fonte de verdade para rotas disponíveis. O Swagger abre em `/docs`. Os schemas propostos para as próximas rotas estão em `apps/api/app/schemas/planned.py`. Quando uma rota for publicada, vincule esses schemas no FastAPI e gere tipos TypeScript do OpenAPI no pacote compartilhado.

| Método e rota         | Situação   | Entrada               | Saída                                                                           |
| --------------------- | ---------- | --------------------- | ------------------------------------------------------------------------------- |
| GET /health           | Disponível | Sem parâmetros        | 200 com Health, objeto com status literal ok. Mede disponibilidade do processo. |
| GET /api/v1/me        | Planejada  | Bearer de sessão      | 200 com Profile, ou 404 até que exista perfil                                   |
| PATCH /api/v1/me      | Planejada  | Bearer e ProfilePatch | 200 com Profile. Cria ou atualiza o perfil a partir do UUID do token.           |
| GET /api/v1/jobs      | Planejada  | JobFilters como query | 200 com JobPage, com items e next_cursor anulável                               |
| GET /api/v1/jobs/{id} | Planejada  | UUID na rota          | 200 com JobDetail, ou 404                                                       |

`Profile` contém id, display_name, headline, location e updated_at. Em `ProfilePatch`, campos omitidos preservam seus valores e null limpa o campo. Campos desconhecidos retornam 422. `JobFilters` aceita q, location, modality, seniority, cursor e limit de 1 a 100, padrão 20. As vagas devem ser ordenadas por publicação decrescente com desempate por UUID e datas ausentes por último. `JobSummary` inclui id, title, company, location, modality, seniority, source e published_at. `JobDetail` acrescenta description e apply_url HTTP(S).

A API devolve `X-Request-ID` em cada resposta. Erros usam `{"error":{"code":"http_404","message":"Not Found"},"request_id":"<uuid>"}`. Rotas autenticadas devem devolver 401 para sessão inválida e 503 se a autenticação estiver indisponível.
