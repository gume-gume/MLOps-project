# 라우터로~
from tkinter import NO
from fastapi import APIRouter,status
from DB.database import SessionLocal
from DB.models import People_Table
from schemas.response import People


router = APIRouter()

db = SessionLocal()

@router.get('/incomes')
def get_all_incomes():
    incomes = db.query(People_Table).all()
    print( 'income ',incomes)    
    return incomes


@router.get('/income/{income_id}',response_model=People, status_code=status.HTTP_200_OK)
def get_an_income(income_id:int):
    try:
        income = db.query(People_Table).filter(People_Table.id == income_id).first()
        return income
    except Exception as err:
        print( 'err',err)
        return err