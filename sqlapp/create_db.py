from database import Base, engine
from models import People

print("Create database ....")

Base.metadata.create_all(engine)