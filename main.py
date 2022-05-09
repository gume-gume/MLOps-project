from fastapi import FastAPI

from routers import redisai

app = FastAPI()


@app.get("/")
def root():
    return "hello world my name is jan"

app.include_router(router=redisai.router)
