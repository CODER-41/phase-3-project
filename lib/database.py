from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = "sqlite://fitness_tracker.db"

engine = create_engine(DATABASE_URL, echo=False)

sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

def get_session():
    return sessionLocal()