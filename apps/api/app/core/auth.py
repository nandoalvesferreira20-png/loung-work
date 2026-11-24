from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient, decode
from jwt.exceptions import (
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)

from app.core.config import Settings, get_settings

bearer = HTTPBearer(auto_error=False)


@lru_cache
def jwks_client(issuer: str) -> PyJWKClient:
    return PyJWKClient(f"{issuer}/.well-known/jwks.json", timeout=5)


def current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UUID:
    unauthorized = HTTPException(
        401, "Credencial inválida ou ausente.", headers={"WWW-Authenticate": "Bearer"}
    )
    if credentials is None:
        raise unauthorized
    if settings.supabase_url is None:
        raise HTTPException(503, "Autenticação indisponível.")
    issuer = f"{str(settings.supabase_url).rstrip('/')}/auth/v1"
    token = credentials.credentials
    try:
        key = jwks_client(issuer).get_signing_key_from_jwt(token)
        claims = decode(
            token,
            key.key,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            issuer=issuer,
            options={"require": ["exp", "iss", "aud", "sub"]},
        )
        if claims.get("role") != "authenticated":
            raise unauthorized
        return UUID(claims["sub"])
    except PyJWKClientConnectionError as exc:
        raise HTTPException(503, "Autenticação indisponível.") from exc
    except (InvalidTokenError, PyJWKClientError, ValueError) as exc:
        raise unauthorized from exc
