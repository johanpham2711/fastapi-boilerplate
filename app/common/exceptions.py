from typing import Any
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppException(HTTPException):
    def __init__(self, status_code: int, message: str, errors: Any = None):
        self.status_code = status_code
        self.detail = message
        self.errors = errors
        super().__init__(status_code=status_code, detail=message)


async def http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": exc.status_code,
            "message": exc.detail if isinstance(exc.detail, str) else "An error occurred",
            "errors": exc.detail if not isinstance(exc.detail, str) else None,
        },
    )


async def validation_exception_handler(request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []
    
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        formatted_errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "code": 422,
            "message": "Validation error",
            "errors": formatted_errors,
        },
    )


async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "code": 500,
            "message": "Internal server error",
            "errors": str(exc) if exc else None,
        },
    )

