from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import encode

from app.core import auth
from app.core.config import Settings

PROJECT_URL = "https://project.example"
ISSUER = f"{PROJECT_URL}/auth/v1"


@pytest.fixture
def jwt_identity(monkeypatch):
    private_key = ec.generate_private_key(ec.SECP256R1())
    jwks = SimpleNamespace(
        get_signing_key_from_jwt=lambda _: SimpleNamespace(key=private_key.public_key())
    )
    monkeypatch.setattr(auth, "jwks_client", lambda _: jwks)
    user_id = uuid4()

    def credential(**overrides):
        claims = {
            "iss": ISSUER,
            "aud": "authenticated",
            "sub": str(user_id),
            "exp": datetime.now(UTC) + timedelta(minutes=5),
            "role": "authenticated",
        }
        token = encode(claims | overrides, private_key, algorithm="ES256")
        return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    return user_id, credential


def test_current_user_id_from_signed_token(jwt_identity):
    user_id, credential = jwt_identity
    assert (
        auth.current_user_id(credential(), Settings(supabase_url=PROJECT_URL))
        == user_id
    )


@pytest.mark.parametrize(
    "claims",
    [
        {"iss": "https://another.example/auth/v1"},
        {"aud": "another-app"},
        {"sub": "invalid-uuid"},
        {"exp": 1},
        {"role": "service_role"},
    ],
)
def test_rejects_invalid_user_claims(jwt_identity, claims):
    _, credential = jwt_identity
    with pytest.raises(HTTPException) as error:
        auth.current_user_id(credential(**claims), Settings(supabase_url=PROJECT_URL))
    assert error.value.status_code == 401
