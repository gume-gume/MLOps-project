from database import Base, engine
from models import People_Table

print("Create database ....")

Base.metadata.create_all(engine)


# 서버 시작할떄 시작..
