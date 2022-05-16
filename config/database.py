from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:1234@localhost/income_db",echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind = engine)


def create_tables():
    print("Create database ....")

    return Base.metadata.create_all(engine)


