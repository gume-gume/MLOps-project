from fastapi import Request
from starlette.responses import JSONResponse

class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f'<AppException {self.exception_case} - '
            + f'status_code={self.status_code} - context={self.context}>'
        )

async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'exception': exc.exception_case,
            'context': exc.context,
        },
    )

class AppException(object):
    class LoadModel(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            load model error
            """
            status_code = 404
            context = '모델 불러오기 실패하였습니다. 모델 명, 모델 키 입력값을 확인하세요.'
            AppExceptionCase.__init__(self, status_code, context)
    class TimeError(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            load time too long
            """
            status_code = 429
            context = '시간이 초과되었습니다.'
            AppExceptionCase.__init__(self, status_code, context)
