from pydantic import BaseModel

class IncomeBody(BaseModel):

    age : int
    workclass : int
    fnlwgt : int
    education : int
    education_num : int
    marital_status : int
    occupation : int
    relationship : int
    race : int
    sex : int
    capital_gain : int
    capital_loss: int
    hours_per_week : int
    native_country : int