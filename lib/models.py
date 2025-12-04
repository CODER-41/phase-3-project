"""
SQLAlchemy ORM Models for Fitness Tracker Application.
Defines User, Workout, Exercise, and WorkoutExercise models with relationships.
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.database import Base

# ============================================================================
# MODEL 1: User
# ============================================================================
class User(Base):
    """
    User model representing individuals using the fitness tracker.
    
    Relationships:
        - Has many Workouts (one-to-many)
    """
    __tablename__ = 'users'
    
    # Primary key - unique identifier for each user
    id = Column(Integer, primary_key=True)
    
    # User information fields
    name = Column(String(100), nullable=False)  # User's full name (required)
    age = Column(Integer, nullable=True)  # Optional age
    weight = Column(Float, nullable=True)  # Optional weight in lbs/kg
    fitness_goal = Column(String(200), nullable=True)  # e.g., "Build muscle", "Lose weight"
    created_at = Column(DateTime, default=datetime.now)  # Account creation timestamp
    
    # Relationship: One user has many workouts
    # cascade='all, delete-orphan' means when a user is deleted, all their workouts are too
    workouts = relationship('Workout', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of User object for debugging"""
        return f"<User(id={self.id}, name='{self.name}', goal='{self.fitness_goal}')>"
    
    def get_all_workouts(self):
        """
        Get all workouts for this user.
        
        Returns:
            list: List of Workout objects
        """
        return self.workouts
    
    def get_workout_count(self):
        """
        Count total number of workouts logged by this user.
        
        Returns:
            int: Total workout count
        """
        return len(self.workouts)
    
    def get_total_exercises_logged(self):
        """
        Count total number of exercises logged across all workouts.
        
        Returns:
            int: Total exercise count
        """
        total = 0
        for workout in self.workouts:
            total += len(workout.workout_exercises)
        return total

# ============================================================================
# MODEL 2: Workout
# ============================================================================
class Workout(Base):
    """
    Workout model representing a single workout session.
    
    Relationships:
        - Belongs to one User (many-to-one)
        - Has many WorkoutExercises (one-to-many)
    """
    __tablename__ = 'workouts'
    
    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Foreign key to User table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Workout information fields
    workout_date = Column(Date, nullable=False)  # Date of workout
    duration = Column(Integer, nullable=True)  # Duration in minutes (optional)
    notes = Column(Text, nullable=True)  # Optional notes about the workout
    created_at = Column(DateTime, default=datetime.now)  # Record creation timestamp
    
    # Relationships
    user = relationship('User', back_populates='workouts')  # Many workouts belong to one user
    workout_exercises = relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of Workout object"""
        return f"<Workout(id={self.id}, user_id={self.user_id}, date={self.workout_date})>"
    
    def add_exercise(self, exercise, sets, reps, weight, notes=None):
        """
        Add an exercise to this workout session.
        
        Args:
            exercise (Exercise): Exercise object to add
            sets (int): Number of sets performed
            reps (int): Number of reps per set
            weight (float): Weight used in lbs/kg
            notes (str, optional): Additional notes
            
        Returns:
            WorkoutExercise: The created WorkoutExercise object
        """
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
        """
        Get all exercises in this workout.
        
        Returns:
            list: List of WorkoutExercise objects
        """
        return self.workout_exercises
    
    def get_total_volume(self):
        """
        Calculate total volume (sets × reps × weight) for entire workout.
        
        Returns:
            float: Total volume lifted
        """
        total_volume = 0
        for we in self.workout_exercises:
            total_volume += we.calculate_volume()
        return total_volume

# ============================================================================
# MODEL 3: Exercise
# ============================================================================
class Exercise(Base):
    """
    Exercise model representing exercise types in the library.
    
    Relationships:
        - Has many WorkoutExercises (one-to-many)
    """
    __tablename__ = 'exercises'
    
    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Exercise information fields
    name = Column(String(100), nullable=False, unique=True)  # Exercise name (must be unique)
    muscle_group = Column(String(50), nullable=False)  # e.g., "Chest", "Back", "Legs"
    equipment_needed = Column(String(100), nullable=True)  # e.g., "Barbell", "Dumbbells"
    description = Column(Text, nullable=True)  # Optional exercise description
    is_custom = Column(Boolean, default=False)  # True if user-created, False if pre-loaded
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationship: One exercise can be used in many workouts
    workout_exercises = relationship('WorkoutExercise', back_populates='exercise')
    
    def __repr__(self):
        """String representation of Exercise object"""
        return f"<Exercise(id={self.id}, name='{self.name}', muscle_group='{self.muscle_group}')>"
    
    @classmethod
    def search_by_name(cls, session, search_term):
        """
        Search for exercises by name (case-insensitive, partial match).
        
        Args:
            session: SQLAlchemy session
            search_term (str): Search query
            
        Returns:
            list: List of matching Exercise objects
        """
        return session.query(cls).filter(
            cls.name.ilike(f"%{search_term}%")
        ).all()
    
    @classmethod
    def filter_by_muscle_group(cls, session, muscle_group):
        """
        Filter exercises by muscle group.
        
        Args:
            session: SQLAlchemy session
            muscle_group (str): Muscle group to filter by
            
        Returns:
            list: List of Exercise objects in that muscle group
        """
        return session.query(cls).filter(
            cls.muscle_group == muscle_group
        ).all()
    
    def get_usage_count(self):
        """
        Count how many times this exercise has been logged.
        
        Returns:
            int: Number of times exercise has been used
        """
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











