from uuid import UUID

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_health_and_openapi():
    with TestClient(create_app(Settings(app_env="test"))) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        assert UUID(response.headers["X-Request-ID"]).version == 4
        assert "/health" in client.get("/openapi.json").json()["paths"]
        assert client.get("/docs").status_code == 200


def test_error_uses_request_id():
    with TestClient(create_app(Settings(app_env="test"))) as client:
        response = client.get("/api/v1/me")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "http_404"
        assert response.json()["request_id"] == response.headers["X-Request-ID"]


def test_cors_only_allows_configured_origin():
    origin = "http://localhost:3000"
    with TestClient(create_app(Settings(cors_origins=[origin]))) as client:
        allowed = client.get("/health", headers={"Origin": origin})
        denied = client.get("/health", headers={"Origin": "https://other.example"})
        assert allowed.headers["Access-Control-Allow-Origin"] == origin
        assert "Access-Control-Allow-Origin" not in denied.headers
