from fastapi import FastAPI

from routers import redisai

app = FastAPI()


@app.get("/")
def root():
    return "소득예측모델"


app.include_router(router=redisai.router)
