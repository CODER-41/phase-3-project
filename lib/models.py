
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.database import Base

class User(Base):
    
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False) 
    age = Column(Integer, nullable=True)  
    weight = Column(Float, nullable=True)  
    fitness_goal = Column(String(200), nullable=True) 
    created_at = Column(DateTime, default=datetime.now) 
    
  
    workouts = relationship('Workout', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):

        return f"<User(id={self.id}, name='{self.name}', goal='{self.fitness_goal}')>"
    
    def get_all_workouts(self):
       
        return self.workouts
    
    def get_workout_count(self):
       
        return len(self.workouts)
    
    def get_total_exercises_logged(self):
     
        total = 0
        for workout in self.workouts:
            total += len(workout.workout_exercises)
        return total

class Workout(Base):
   
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    workout_date = Column(Date, nullable=False)  
    duration = Column(Integer, nullable=True) 
    notes = Column(Text, nullable=True)  
    created_at = Column(DateTime, default=datetime.now)  

    user = relationship('User', back_populates='workouts')  
    workout_exercises = relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    def __repr__(self):
    
        return f"<Workout(id={self.id}, user_id={self.user_id}, date={self.workout_date})>"
    
    def add_exercise(self, exercise, sets, reps, weight, notes=None):
    
        workout_exercise = WorkoutExercise(
            workout=self,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=weight,
            notes=notes
        )
        return workout_exercise
    
    def get_all_exercises(self):
     
        return self.workout_exercises
    
    def get_total_volume(self):
      
        total_volume = 0
        for we in self.workout_exercises:
            total_volume += we.calculate_volume()
        return total_volume

class Exercise(Base):

    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    

    name = Column(String(100), nullable=False, unique=True)  
    muscle_group = Column(String(50), nullable=False)  
    equipment_needed = Column(String(100), nullable=True)  
    description = Column(Text, nullable=True)  
    is_custom = Column(Boolean, default=False)  
    created_at = Column(DateTime, default=datetime.now)
    
    
    workout_exercises = relationship('WorkoutExercise', back_populates='exercise')
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', muscle_group='{self.muscle_group}')>"
    
    @classmethod
    def search_by_name(cls, session, search_term):
        
        return session.query(cls).filter(
            cls.name.ilike(f"%{search_term}%")
        ).all()
    
    @classmethod
    def filter_by_muscle_group(cls, session, muscle_group):
       
        return session.query(cls).filter(
            cls.muscle_group == muscle_group
        ).all()
    
    def get_usage_count(self):
        
        return len(self.workout_exercises)

# ============================================================================
# MODEL 4: WorkoutExercise (Association/Join Table with Extra Data)
# ============================================================================
class WorkoutExercise(Base):
    """
    WorkoutExercise model - join table between Workout and Exercise.
    This table also stores workout-specific data (sets, reps, weight).
    
    Relationships:
        - Belongs to one Workout (many-to-one)
        - Belongs to one Exercise (many-to-one)
    """
    __tablename__ = 'workout_exercises'
    
    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Foreign keys
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    
    # Exercise performance data
    sets = Column(Integer, nullable=False)  # Number of sets performed
    reps = Column(Integer, nullable=False)  # Number of reps per set
    weight = Column(Float, nullable=False)  # Weight used in lbs/kg
    notes = Column(Text, nullable=True)  # Optional notes
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    workout = relationship('Workout', back_populates='workout_exercises')
    exercise = relationship('Exercise', back_populates='workout_exercises')
    
    def __repr__(self):
        """String representation of WorkoutExercise object"""
        return f"<WorkoutExercise(id={self.id}, exercise='{self.get_exercise_name()}', {self.sets}x{self.reps}@{self.weight}lbs)>"
    
    def calculate_volume(self):
        """
        Calculate total volume (sets × reps × weight) for this exercise.
        
        Returns:
            float: Volume lifted
        """
        return self.sets * self.reps * self.weight
    
    def get_exercise_name(self):
        """
        Get the name of the exercise.
        
        Returns:
            str: Exercise name
        """
        return self.exercise.name if self.exercise else "Unknown"











