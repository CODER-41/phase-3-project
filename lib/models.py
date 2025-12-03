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
    
    def get_workout_count(self):
        return len(self.workouts)
    
    def get_total_exercise_logged(self):
        total = 0
        for workout in self.workouts:
            total += len(workout.workout_exercises)
        
        return total
    

class Workout(Base):

    __tablename__ = 'workouts'

    id = Column(Integer, ForeignKey('users.id'), nullable=False)

    workout_date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


    user = relationship('User', back_poulates='workouts')
    workout_exercises = relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')


    def __repr__(self):
        return f"<Workout(id={self.id}, user_id={self.user_id}, date={self.workout_date})>"
    

    def add_exercise(self, exercise, sets, reps, weight, notes=None):