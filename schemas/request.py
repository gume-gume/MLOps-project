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