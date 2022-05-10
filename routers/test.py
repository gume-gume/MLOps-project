from fastapi import APIRouter, Body 
from schemas.request import RequestBody
from schemas.response import ResponseBody



router = APIRouter()

@router.post('/test/{param1}', response_model=ResponseBody)
def test(param1: str, param2: int, body: RequestBody = Body(...)):
    return {"param1": param1, "param2": param2, "body": body}
