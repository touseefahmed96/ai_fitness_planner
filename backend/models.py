from database import Base
from sqlalchemy import Column, Float, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    weight = Column(Float, default=0)
    height = Column(Float, default=0)
    goal = Column(String, default="fitness")
