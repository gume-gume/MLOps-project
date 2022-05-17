from fastapi import FastAPI
from routers import redisai

# exception handler
from errors.exception import *
from errors.handlers import validation_exception_handler, custom_500_handler


from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

app = FastAPI()

app.include_router(router=redisai.router)

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(500, custom_500_handler)
