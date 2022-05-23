from fastapi import FastAPI
from routers import income

# exception handler
from utils.handlers import *
from fastapi.exceptions import RequestValidationError
from utils.app_exceptions import AppExceptionCase
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.include_router(router=income.router)

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(AppExceptionCase, custom_app_exception_handler)
