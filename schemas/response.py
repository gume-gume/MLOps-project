from pydantic import BaseModel

from schemas.request import RequestBody


class ResponseBody(BaseModel):
    param1: str
    param2: int
    body: RequestBody
