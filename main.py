from fastapi import FastAPI
from routers import id
from routers import test
from routers import redisai
from sqlapp import main



app = FastAPI()

@app.get('/')
def root():
    return "Welcome to gume-gume"

app.include_router(router=test.router)
app.include_router(router=main.router) 
app.include_router(router=id.router)
app.include_router(router=redisai.router)


