from tkinter import NO
from fastapi import APIRouter,status, HTTPException
from pydantic import BaseModel
from typing import List
from .database import SessionLocal
from sqlapp.models import People

router = APIRouter()

class People(BaseModel):
    id : int
    workclass : str
    fnlwgt : int
    education : str
    education_num : int
    marital_status : str
    occupation : str
    relationship : str
    race : str
    sex : str
    capital_gain : int
    capital_loss : int
    hours_per_week : int
    native_country : str
    
    target : int

    class Config:
        orm_mode = True

db = SessionLocal()
print('db', db)

@router.get('/incomes', response_model=List[People],status_code=200)
def get_all_incomes():
    incomes = db.query(People).all()
    return incomes

@router.get('/income/{income_id}',response_model=People, status_code=status.HTTP_200_OK)
def get_an_income(income_id:int):
    try:
        # income = db.query(People).filter(People.id == income_id).first()
        income = db.query(People)
        return income
    except Exception as err:
        print( 'err',err)
        return err

@router.post('/incomes',response_model=People, status_code=status.HTTP_201_CREATED)
def create_an_income(income:People):
    new_income = People(
        workclass = income.workclass,
        fnlwgt    = income.fnlwgt,
        education = income.education,
        education_num = income.education_num,
        marital_status = income.marital_status,
        occupation = income.occupation,
        relationship = income.relationship,
        race = income.race,
        sex = income.sex,
        capital_gain = income.capital_gain,
        capital_loss = income.capital_loss,
        hours_per_week = income.hours_per_week,
        native_country = income.native_country
    )

    db.add(new_income)
    db.commit()

    return new_income

@router.put('/income/{income_id}',response_model=People, status_code=status.HTTP_200_OK)
def update_an_income(income_id:int,income:People):
    income_to_update = db.query(People).filter(People.id == income_id).first()
    income_to_update.workclass  = income.workclass
    income_to_update.fnlwgt  = income.fnlwgt
    income_to_update.education  = income.education
    income_to_update.education_num  = income.education_num
    income_to_update.marital_status  = income.marital_status
    income_to_update.occupation  = income.occupation
    income_to_update.relationship  = income.relationship
    income_to_update.race  = income.race
    income_to_update.sex  = income.sex
    income_to_update.capital_gain  = income.capital_gain
    income_to_update.capital_loss  = income.capital_loss
    income_to_update.hours_per_week  = income.hours_per_week
    income_to_update.native_country  = income.native_country

    db.commit()

    return income_to_update

@router.delete('income/{income_id}')
def delete_income(income_id:int):
    income_to_delete = db.query(People).filter(People.id == income_id).first()

    if income_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Resource Not Found')
    
    db.delete(income_to_delete)
    db.commit()

    return income_to_delete
