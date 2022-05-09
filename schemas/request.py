from fastapi import FastAPI
from pydantic import BaseModel


class RequestBody(BaseModel):
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_pre_week: int
    native_country: str
    target: int



