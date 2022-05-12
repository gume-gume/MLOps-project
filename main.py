from fastapi import FastAPI
from routers import redisai, db

app = FastAPI()

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.include_router(router=db.router) 
app.include_router(router=redisai.router)


