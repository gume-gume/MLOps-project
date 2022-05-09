from fastapi import FastAPI
from pydantic import BaseModel
from schemas.request import RequestBody

class ResponseBody(BaseModel):
    id: str
    body: RequestBody