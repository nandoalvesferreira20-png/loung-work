# Arquitetura

O Next.js cuida da experiência web. A FastAPI concentra regras de domínio, validação e persistência. O pacote `@loung/api-client` isola o transporte HTTP para que o frontend evolua contra o contrato da API. O [contrato inicial](api-contract.md) diferencia endpoints disponíveis de propostas.

As rotas de domínio entram em `app/api/v1`, casos de uso em `services`, persistência em `repositories` e entidades SQLAlchemy em `models`. O Supabase emite os tokens de sessão. A API valida assinatura, emissor, público, expiração e papel antes de extrair o UUID da sessão. A [documentação do Supabase](https://supabase.com/docs/guides/auth/signing-keys) descreve o JWKS usado pela integração.

Cada conector futuro em `app/connectors` deverá normalizar resultados de uma fonte autorizada e preservar identificador da fonte, origem e link de candidatura. Defina limites de chamadas e regras de atualização com base no acordo de cada fonte. A persistência deve usar identidade por fonte e importações idempotentes.
