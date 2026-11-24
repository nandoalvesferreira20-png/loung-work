import json
import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.api.v1.router import router
from app.core.config import Settings, get_settings
from app.schemas.health import Health

logger = logging.getLogger("uvicorn.error")


def error_response(
    request: Request, status: int, code: str, message: str, headers=None
):
    return JSONResponse(
        status_code=status,
        headers=headers,
        content={
            "error": {"code": code, "message": message},
            "request_id": request.state.request_id,
        },
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or get_settings()
    api = FastAPI(title="Loung Work API", version="0.1.0")
    if settings is not None:
        api.dependency_overrides[get_settings] = lambda: config
    api.include_router(router)

    @api.middleware("http")
    async def request_context(request: Request, call_next):
        request.state.request_id = str(uuid4())
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                json.dumps(
                    {
                        "event": "request.failed",
                        "request_id": request.state.request_id,
                        "exception_type": type(exc).__name__,
                    }
                )
            )
            response = error_response(request, 500, "internal_error", "Erro interno.")

        response.headers["X-Request-ID"] = request.state.request_id
        route = request.scope.get("route")
        logger.info(
            json.dumps(
                {
                    "event": "request.completed",
                    "request_id": request.state.request_id,
                    "method": request.method,
                    "route": getattr(route, "path", None),
                    "status": response.status_code,
                    "duration_ms": round((perf_counter() - started) * 1000, 2),
                }
            )
        )
        return response

    api.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["X-Request-ID"],
    )

    @api.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return error_response(
            request,
            exc.status_code,
            f"http_{exc.status_code}",
            str(exc.detail),
            exc.headers,
        )

    @api.exception_handler(RequestValidationError)
    async def validation_error(request: Request, _exc: RequestValidationError):
        return error_response(request, 422, "validation_error", "Dados inválidos.")

    @api.get("/health", tags=["Operação"])
    def health() -> Health:
        return Health()

    return api


app = create_app()
