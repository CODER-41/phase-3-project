from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    age = Column(Integer)
    weight = Column(Float)
    fitness_goal = Column(String)
    created_at = Column(DateTime, default=datetime.now )