from .database import Base
from sqlalchemy import String,Integer,Column

class People(Base):
    __tablename__ = 'people_income'

    id = Column(Integer,primary_key=True)
    age = Column(Integer)
    workclass = Column(String(20))
    fnlwgt = Column(Integer)
    education = Column(String(20))
    education_num = Column(Integer)
    marital_status = Column(String(40))
    occupation = Column(String(20))
    relationship = Column(String(40))
    race =  Column(String(20))
    sex = Column(String(6))
    capital_gain = Column(Integer)
    capital_loss = Column(Integer)
    hours_per_week = Column(Integer)
    native_country = Column(String(40))
    
    target = Column(Integer)

    def __repr__(self):
        return f'<People \
                  age = {self.age} workclass = {self.workclass} \
                  fnlwgt = {self.fnlwgt} education = {self.education} \
                  education_num = {self.education_num} marital_status = {self.marital_status} \
                  occupation = {self.occupation} relationship = {self.relationship} \
                  race = {self.race} sex = {self.sex} \
                  capital_gain = {self.capital_gain} capital_loss = {self.capital_loss} \
                  hours_per_week = {self.hours_per_week} native_country = {self.native_country} >' 
