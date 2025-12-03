from datetime import datetime, date
from lib.models import user, EXercise, Workout, WorkoutExercise

def clear_screen():
    print("\n" * 50)


def print_header(text):

    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_subheader(text):

    print("\n" + "-"*60)
    print(f"  {text}")
    print("-"*60)


def get_valid_integer(prompt, min_value=None, max_value=None):
 
    while True:
        try:
            value = int(input(prompt))
            
            if min_value is not None and value < min_value:
                print(f"Please enter a number >= {min_value}")
                continue
            
            if max_value is not None and value > max_value:
                print(f" Please enter a number <= {max_value}")
                continue
            
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_float(prompt, min_value=None):
  
    while True:
        try:
            value = float(input(prompt))

            if min_value is not None and value < min_value:
                print(f" Please enter a number >= {min_value}")
                continue
            
            return value
        except ValueError:
            print(" Invalid input. Please enter a valid number.")

def get_valid_date(prompt):

    while True:
        date_str = input(prompt)
        
        if date_str.lower() == 'today':
            return date.today()
        
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return parsed_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (or type 'today')")

def format_workout_summary(workout):
    exercise_lines = []
    
    for we in workout.workout_exercises:
        exercise_lines.append(
            f" {we.get_exercise_name()}: {we.sets}x{we.reps} @ {we.weight}lbs"
        )
    
    exercises_str = "\n".join(exercise_lines) if exercise_lines else "    (No exercises logged)"
    
    summary = f"""
  Date: {workout.workout_date}
  Exercises: {len(workout.workout_exercises)}
  Total Volume: {workout.get_total_volume():.1f} lbs
{exercises_str}
"""
    return summary

def display_exercise_list(exercises):
    if not exercises:
        print("  No exercises found.")
        return
    
    print(f"\n  Found {len(exercises)} exercise(s):\n")

    for idx, exercise in enumerate(exercises, 1):
        print(f"  {idx}. {exercise.name}")
        print(f"     Muscle Group: {exercise.muscle_group}")
        print(f"     Equipment: {exercise.equipment_needed or 'None'}")
        if exercise.description:
            print(f"     Description: {exercise.description}")
        print()

def get_exercise_choice(session, exercises):

    if not exercises:
        return None
    
    while True:
        choice = input(f"\n  Select exercise (1-{len(exercises)}, or 0 to cancel): ").strip()
        
        if choice == '0':
            return None
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(exercises):
                return exercises[idx]
            else:
                print(f"Please enter a number between 1 and {len(exercises)}")
        except ValueError:
            print("✗ Invalid input. Please enter a number.")

def confirm_action(prompt="Are you sure?"):
  
    response = input(f"\n  {prompt} (y/n): ").strip().lower()
    return response in ['y', 'yes']

# ============================================================================
# FILE 6: lib/cli.py
# ============================================================================
# This is the main CLI interface file

"""
Main CLI Interface for Fitness Tracker Application.
Provides interactive command-line interface for all application features.
"""

import sys
from datetime import date
from lib.database import init_db, get_session
from lib.models import User, Exercise, Workout, WorkoutExercise
from lib.seed import seed_database
from lib.helpers import (
    clear_screen, print_header, print_subheader,
    get_valid_integer, get_valid_float, get_valid_date,
    format_workout_summary, display_exercise_list,
    get_exercise_choice, confirm_action
)

# Global variable to store current active user
current_user = None

# ============================================================================
# USER MANAGEMENT FUNCTIONS
# ============================================================================

def create_user(session):
    """
    Create a new user account.
    
    Args:
        session: SQLAlchemy session
    """
    print_subheader("Create New User")
    
    # Get user information
    name = input("\n  Enter your name: ").strip()
    if not name:
        print("✗ Name cannot be empty.")
        return
    
    # Optional fields with default values
    age_input = input("  Enter your age (optional, press Enter to skip): ").strip()
    age = int(age_input) if age_input else None
    
    weight_input = input("  Enter your weight in lbs (optional, press Enter to skip): ").strip()
    weight = float(weight