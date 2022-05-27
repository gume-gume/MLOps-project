from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import income
from schemas.response import error_responses
# exception handler
from utils.handlers import *
from fastapi.exceptions import RequestValidationError
from utils.app_exceptions import AppExceptionCase
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(responses={**error_responses}) ## --> 에러 500, 404,422,429 Not found 정의

app.include_router(router=income.router)

@app.get('/')
def root():
    return 'Welcome to gume-gume'

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(AppExceptionCase, custom_app_exception_handler)
