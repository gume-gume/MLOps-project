from fastapi import FastAPI
from routers import redisai

app = FastAPI()

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.include_router(router=redisai.router)