from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    print('asdasdasfda',exc.status_code)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "exception": exc.errors()[0]['type'],
            "context": '입력 값 오류입니다. 입력값을 확인하세요.'
        }
    )
