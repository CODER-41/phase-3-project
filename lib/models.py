from sqlalchemy import Column, Integer, String, Float, Date, DateTime,  Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable = False)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    fitness_goal = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.now )

    workouts = relationship('Workout', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', goal='{self.fitness_goal}')>"
    
    def get_all_workouts(self):
        return self.workouts
    
    def get_total_exercise_logged(self):
        total = 0
        for workout in self.workouts:
            total += len(workout.workout_exercises)
        
        return total