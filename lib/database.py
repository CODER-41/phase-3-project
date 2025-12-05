from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = "sqlite:///fitness_tracker.db"

engine = create_engine(
    DATABASE_URL, 
    echo=False,
    connect_args = {"check_same_thread": False}
)

sessionLocal = sessionmaker(bind = engine)

def init_db():
    from lib.models import User, Workout, Exercise, WorkoutExercise

    Base.metadata.create_all(bind=engine)
    print("Database initialized sussessfully!")



def get_session():
    return sessionLocal()