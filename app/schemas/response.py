from pydantic import BaseModel
from typing import Optional


class People(BaseModel):
    """
    작성자 : 장영동
    response 모델
    """

    id: int
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
    hours_per_week: int
    native_country: str
    target: int

    class Config:
        orm_mode = True


class TrainDone(BaseModel):
    purpose: str
    context: str


class Item(BaseModel):
    """
    작성자 : 장영동
    prediction output
    """

    target: int
    context: Optional[str] = None


class Coin_pred(BaseModel):

    price: int
    context: Optional[str] = None


class ExceptionResponseModel(BaseModel):
    exception: str
    context: str
