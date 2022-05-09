from fastapi import APIRouter, Body, Response
from schemas.request import RequestBody
from schemas.response import ResponseBody

router = APIRouter()

@router.post('/id/{param1}', response_model=ResponseBody)
def id(param1: int, body: RequestBody = Body(...)):
    return {"param1": param1, "body": body}