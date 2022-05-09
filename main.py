from fastapi import FastAPI
from routers import id


app = FastAPI()

@app.get('/')
def hello():
    return "Hello World"

app.include_router(router=id.router)