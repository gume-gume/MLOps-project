from fastapi.responses import JSONResponse

from fastapi.responses import PlainTextResponse



async def custom_500_handler(request, __):
    return JSONResponse(
        status_code=500,
        content={"message": "500 error..... Run Docker"},
    )


async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)
