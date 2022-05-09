from pydantic import BaseModel


class RequestBody(BaseModel):
    model: str
    cc: int


class IncomeBody(BaseModel):
    age: float
    workclass:float
    fnlwgt:float
    education:float
    marital_status:float
    occupation:float
    relationship:float
    race:float
    sex:float
    hours_per_week:float
    native_country:float
    capital:float
    high_educated:float
    Marriage:float
    high_income:float
    family:float