from pydantic import BaseModel
from typing import Optional

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
    target : Optional[int] = None
    context : Optional[str] = None
class MakeModel(BaseModel):
    n_trial : int
    n_split : int
    scoring : str
