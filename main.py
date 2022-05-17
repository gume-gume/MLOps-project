from fastapi import FastAPI
from routers import redisai

# exception handler
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException

app = FastAPI()

app.include_router(router=redisai.router)

@app.get('/')
def root():
    return "Welcome to gume-gume"

@app.exception_handler(500)
async def custom_404_handler(request, __):
    return JSONResponse(
        status_code=500,
        content={"message": "500 error..... Run Docker"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print('call..')
    return PlainTextResponse(str(exc), status_code=422)