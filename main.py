from fastapi import FastAPI
from routers import id
from routers import redisai

app = FastAPI()

@app.get('/')
def hello():
    return "소득예측모델"

app.include_router(router=id.router)
app.include_router(router=redisai.router)




