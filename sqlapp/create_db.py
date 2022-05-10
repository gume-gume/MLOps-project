from database import Base, engine



print("Create database ....")

Base.metadata.create_all(engine)