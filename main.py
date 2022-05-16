from fastapi import FastAPI, HTTPException, status
from routers import redisai
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from utils.exceptions import *
from utils.exception_handlers import *


app = FastAPI()

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.include_router(router=redisai.router)


app.add_exception_handler(HTTPException, http_exception_handler)
