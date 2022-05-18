from fastapi.responses import JSONResponse

from fastapi.responses import PlainTextResponse

from errors.app_exceptions import AppExceptionCase
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from errors.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from errors.app_exceptions import app_exception_handler

async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)

async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)

async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)

async def custom_500_handler(request, __):
    return JSONResponse(
        status_code=500,
        content={"message": "500 error..... Run Docker"},
    )
