from pydantic import BaseModel
from typing import Optional
from enum import Enum


class IncomeBody(BaseModel):
    """
    작성자 : 장영동
    request body / input data
    """

    age: int
    workclass: int
    fnlwgt: int
    education: int
    education_num: int
    marital_status: int
    occupation: int
    relationship: int
    race: int
    sex: int
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: int
    target: Optional[int] = None
    context: Optional[str] = None


class MakeModel(BaseModel):
    """
    작성자 : 장영동
    모델 학습 파라미터
    """

    n_trial: int
    n_split: int
    scoring: str


class ModelName(str, Enum):
    BTC = ("KRW-BTC",)
    ETH = ("KRW-ETH",)
    ADA = "KRW-ADA"
