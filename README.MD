## Fitness Tracker & Workout Planner
A comprehensive command-line interface (CLI) application for tracking workouts, exercises, and fitness progress using Python and SQLALchemy ORM.

## Table of Contents
- [Features]
- [Testing the Application]
- [Future Enhancements]
-[Installation]
- [License](#license)
- [Authors](#Authors)
- [Contact Information](#contact-information)

## Features

- User Management
    .Create multiple user profile
    .Switch between users
    . Track individual progress
    
- Workout Logging
    .Log workout sessions with date
    .Add multiple exercise per workout
    .Record sets, reps, and weight
    .Add notes for workouts and exercise
    
- Exercise Library
    .Pre-loaded with 40+ common exercise
    .Organized by 7 muscle groups
    .Search by name or muscle group
    .Add custom exercise
    
- Progress Tracking
    .View complete workout history
    .Track exercise-specific progress
    .See personal records
    .Calculate workout statistics
    
- Statistics
    .Total workouts and exercises
    .Total volume lifted
    .Workout frequently 
    .Most trained exercises
    


## Testing the Application 
- Test Scenario 1: New User Journey
    .Run application
    .Create new user
    .Log a workout with 2-3 exercises
    .View workout history
    .Check statistics

- Test Scenario 2: Multiple Users
    .Create User A and log workouts
    .Create User B and log different workouts
    .Switch between users
    .Verify data separation

- Test Scenario 3: Exercise Library
    .Search for exercises by name
    .Browse exercises by muscle group
    .Add a custom exercise
    .Use custom exercise in workout

##Future Enhancements
    .Export workout data to CSV(Coma -Separated Values)
    .Body weight tracking over time
    .Workout templates/programs
    .Progress charts (ASCII art)
    .Rest timer between sets
    .Volume calculations and analytics
    .Exercise form videos/tips
    .Nutrition tracking integration


## Installation
 - Install Pipenv(if not already installed)
 bash: pip install pipenv
 
- Install dependencies:
    bash:
        pipenv install
- Activate Virtual Environment
    bash: pipenv shell
    
- Run the Application
    bash: python -m lib.cli


## License
Educational project 

## Authors
- Created as a Python CLI + ORM project demonstrating:

- SQLAlchemy ORM mastery
- CLI application developments
- Database design and relationships
- Real-world problem solving

 
 #Ronny Mboya

## Contact Information
* Email : mboyaronnny41@gmail.com