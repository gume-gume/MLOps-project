from fastapi import FastAPI
from routers import test
from sqlapp import main

app = FastAPI()

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.include_router(router=test.router)
app.include_router(router=main.router) 