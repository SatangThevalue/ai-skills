# FastAPI Global Exception Handling Pattern

This template implements a robust, production-grade exception handling framework for FastAPI applications using `structlog` and SQLModel/SQLAlchemy.

## File Structure

Create this file at `app/core/exceptions.py`.

```python
import sys
import structlog
from typing import Any
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

logger = structlog.get_logger()

class AppBaseException(Exception):
    """Base application exception for business rule violations."""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "BAD_REQUEST",
        details: Any = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(message)


def create_error_response(
    status_code: int,
    error_code: str,
    message: str,
    details: Any = None
) -> JSONResponse:
    """Helper to return consistent JSON error formats."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
                "details": details or {}
            }
        }
    )


async def app_exception_handler(request: Request, exc: AppBaseException) -> JSONResponse:
    logger.warn(
        "Application business rule exception occurred",
        path=request.url.path,
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details
    )
    return create_error_response(
        status_code=exc.status_code,
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details
    )


async def fastapi_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    logger.warn(
        "HTTP exception occurred",
        path=request.url.path,
        status_code=exc.status_code,
        detail=exc.detail
    )
    error_codes = {
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED"
    }
    error_code = error_codes.get(exc.status_code, "HTTP_ERROR")
    return create_error_response(
        status_code=exc.status_code,
        error_code=error_code,
        message=str(exc.detail)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    formatted_errors = []
    for err in errors:
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        formatted_errors.append({
            "field": field,
            "type": err.get("type"),
            "msg": err.get("msg")
        })
        
    logger.info(
        "Request validation failed",
        path=request.url.path,
        errors=formatted_errors
    )
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        message="Request payload parameters validation failed.",
        details=formatted_errors
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(
        "Database exception occurred",
        path=request.url.path,
        error=str(exc),
        exc_info=sys.exc_info()
    )
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="DATABASE_ERROR",
        message="A database system error occurred. Please try again later."
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled system exception occurred",
        path=request.url.path,
        error=str(exc),
        exc_info=sys.exc_info()
    )
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected system error occurred. Our team has been notified."
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppBaseException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, fastapi_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
```

## Setup in main.py

Import and register the setup function right after instantiating `FastAPI`:

```python
from app.core.exceptions import setup_exception_handlers

app = FastAPI(...)
setup_exception_handlers(app)
```
