import uvicorn
from fastapi import FastAPI
from routers import income
from schemas.response import ExceptionResponseModel
from utils.handlers import (
    custom_http_exception_handler,
    custom_validation_exception_handler,
    custom_app_exception_handler,
)

from utils.app_exceptions import AppExceptionCase
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    responses={
        404: {"model": ExceptionResponseModel, "description": "Additional Response"},
        422: {"model": ExceptionResponseModel, "description": "Validation Error"},
        429: {"model": ExceptionResponseModel, "description": "Time Out Error"},
        500: {"model": ExceptionResponseModel, "description": "Internal Server Error"},
    }
)

app.include_router(router=income.router)


@app.get("/")
def root():
    return "Welcome to gume-gume"


app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(AppExceptionCase, custom_app_exception_handler)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
