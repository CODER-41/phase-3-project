
import sys
import os
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


current_user = None


def create_user(session):
   
    print_subheader("Create New User")
    
    name = input("\n  Enter your name: ").strip()
    if not name:
        print(" Name cannot be empty.")
        return
    
    age_input = input("  Enter your age (optional, press Enter to skip): ").strip()
    age = int(age_input) if age_input else None
    
    weight_input = input("  Enter your weight in lbs (optional, press Enter to skip): ").strip()
    weight = float(weight_input) if weight_input else None
    
    fitness_goal = input("  Enter your fitness goal (optional, press Enter to skip): ").strip()
    fitness_goal = fitness_goal if fitness_goal else None
    
    new_user = User(
        name=name,
        age=age,
        weight=weight,
        fitness_goal=fitness_goal
    )
    
    session.add(new_user)
    session.commit()
    
    print(f"\n User '{name}' created successfully! (ID: {new_user.id})")
    
    
    global current_user
    current_user = new_user
    print(f" '{name}' is now the active user.")

def list_users(session):
  
    users = session.query(User).all()
    
    if not users:
        print("\n  No users found. Create a user first!")
        return []
    
    print(f"\n  Total Users: {len(users)}\n")

    for idx, user in enumerate(users, 1):
        print(f"  {idx}. {user.name} (ID: {user.id})")
        if user.age:
            print(f"     Age: {user.age}")
        if user.weight:
            print(f"     Weight: {user.weight} lbs")
        if user.fitness_goal:
            print(f"     Goal: {user.fitness_goal}")
        print(f"     Workouts: {user.get_workout_count()}")
        print()
    
    return users

def switch_user(session):

    print_subheader("Switch User")
    
    users = list_users(session)
    
    if not users:
        return
    
    choice = get_valid_integer(
        f"\n  Select user (1-{len(users)}, or 0 to cancel): ",
        min_value=0,
        max_value=len(users)
    )
    
    if choice == 0:
        print("  Cancelled.")
        return
    
    global current_user
    current_user = users[choice - 1]
    print(f"\n Switched to user: {current_user.name}")

def user_management_menu(session):

    while True:
        print_subheader("User Management")
        
        
        if current_user:
            print(f"\n  Current User: {current_user.name}")
        else:
            print("\n  No user selected")
        
        print("\n  1. Create New User")
        print("  2. List All Users")
        print("  3. Switch User")
        print("  0. Back to Main Menu")
        
        choice = input("\n  Enter choice: ").strip()
        
        if choice == '1':
            create_user(session)
        elif choice == '2':
            list_users(session)
            input("\n  Press Enter to continue...")
        elif choice == '3':
            switch_user(session)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def log_workout(session):
   
    if not current_user:
        print("\n Please select or create a user first!")
        return
    
    print_subheader(f"Log New Workout - {current_user.name}")

    print("\n  Enter workout date (YYYY-MM-DD or 'today'):")
    workout_date = get_valid_date("  Date: ")
    
    notes = input("\n  Workout notes (optional, press Enter to skip): ").strip()
    notes = notes if notes else None
    

    workout = Workout(
        user=current_user,  
        workout_date=workout_date,
        notes=notes
    )
    session.add(workout)
    
    print(f"\n Workout session created for {workout_date}")
    print("\n  Now let's add exercises to this workout...")

    while True:
        print("\n" + "-"*60)
        print("  Add Exercise")
        print("-"*60)
        
    
        search_term = input("\n  Search exercise by name (or 'cancel' to finish): ").strip()
        
        if search_term.lower() == 'cancel':
            break
        
        exercises = Exercise.search_by_name(session, search_term)
        
        if not exercises:
            print(f"\n  No exercises found matching '{search_term}'")
            
            
            if confirm_action("Would you like to browse by muscle group?"):
                exercise = browse_exercises_by_muscle_group(session)
                if not exercise:
                    continue
            else:
                continue
        else:
    
            display_exercise_list(exercises)
    
            exercise = get_exercise_choice(session, exercises)
            
            if not exercise:
                continue
    
        print(f"\n  Adding: {exercise.name}")
        sets = get_valid_integer("  Sets: ", min_value=1)
        reps = get_valid_integer("  Reps: ", min_value=1)
        weight = get_valid_float("  Weight (lbs): ", min_value=0)
        
        exercise_notes = input("  Notes (optional, press Enter to skip): ").strip()
        exercise_notes = exercise_notes if exercise_notes else None
    
        workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=weight,
            notes=exercise_notes
        )
        session.add(workout_exercise)
        
        print(f"\n Added: {exercise.name} - {sets}x{reps} @ {weight}lbs")
        
    
        if not confirm_action("Add another exercise?"):
            break
    
    session.commit()
    

    print("\n" + "="*60)
    print("  WORKOUT SUMMARY")
    print("="*60)
    print(format_workout_summary(workout))
    print(f"\n✓ Workout logged successfully! (ID: {workout.id})")

def browse_exercises_by_muscle_group(session):
  
    muscle_groups = ('Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core', 'Cardio')
    
    print("\n  Select Muscle Group:")
    for idx, mg in enumerate(muscle_groups, 1):
        print(f"  {idx}. {mg}")
    print("  0. Cancel")
    
    choice = get_valid_integer(
        f"\n  Enter choice (0-{len(muscle_groups)}): ",
        min_value=0,
        max_value=len(muscle_groups)
    )
    
    if choice == 0:
        return None
    
    selected_muscle_group = muscle_groups[choice - 1]
    
    exercises = Exercise.filter_by_muscle_group(session, selected_muscle_group)
    
    if not exercises:
        print(f"\n  No exercises found for {selected_muscle_group}")
        return None
    

    display_exercise_list(exercises)
    return get_exercise_choice(session, exercises)

def view_workout_history(session):

    if not current_user:
        print("\n Please select or create a user first!")
        return
    
    print_subheader(f"Workout History - {current_user.name}")
    
    
    workouts = current_user.get_all_workouts()
    
    if not workouts:
        print("\n  No workouts logged yet. Start logging workouts!")
        return
    

    sorted_workouts = sorted(workouts, key=lambda w: w.workout_date, reverse=True)
    
    print(f"\n  Total Workouts: {len(sorted_workouts)}")
    print(f"  Total Exercises Logged: {current_user.get_total_exercises_logged()}")

    for idx, workout in enumerate(sorted_workouts, 1):
        print("\n" + "="*60)
        print(f"  WORKOUT #{idx}")
        print("="*60)
        print(format_workout_summary(workout))
        
        if workout.notes:
            print(f"  Notes: {workout.notes}")
    
    input("\n  Press Enter to continue...")

def view_exercise_history(session):
   
    if not current_user:
        print("\n Please select or create a user first!")
        return
    
    print_subheader(f"Exercise History - {current_user.name}")

    search_term = input("\n  Search exercise by name: ").strip()
    
    if not search_term:
        print("✗ Search term cannot be empty.")
        return

    exercises = Exercise.search_by_name(session, search_term)
    
    if not exercises:
        print(f"\n  No exercises found matching '{search_term}'")
        return
    
    
    display_exercise_list(exercises)
    exercise = get_exercise_choice(session, exercises)
    
    if not exercise:
        return
    

    workout_exercises = session.query(WorkoutExercise).join(
        Workout
    ).filter(
        Workout.user_id == current_user.id,
        WorkoutExercise.exercise_id == exercise.id
    ).order_by(
        Workout.workout_date.desc()
    ).all()
    
    if not workout_exercises:
        print(f"\n  No history found for {exercise.name}")
        return
    
    print("\n" + "="*60)
    print(f"  EXERCISE HISTORY: {exercise.name}")
    print("="*60)
    print(f"\n  Total Sessions: {len(workout_exercises)}")
    

    max_weight = max([we.weight for we in workout_exercises])
    print(f"  Personal Record: {max_weight} lbs")
    
    
    print("\n  Session History:")
    for idx, we in enumerate(workout_exercises, 1):
        print(f"\n  {idx}. Date: {we.workout.workout_date}")
        print(f"     {we.sets} sets × {we.reps} reps @ {we.weight} lbs")
        print(f"     Volume: {we.calculate_volume()} lbs")
        if we.notes:
            print(f"     Notes: {we.notes}")
    
    input("\n  Press Enter to continue...")

def view_statistics(session):
    """
    Display workout statistics for current user.
    Shows totals, averages, and most trained exercises.
    
    Args:
        session: SQLAlchemy session
    """
    # Check if user is logged in
    if not current_user:
        print("\n✗ Please select or create a user first!")
        return
    
    print_subheader(f"Statistics - {current_user.name}")
    
    workouts = current_user.get_all_workouts()
    
    if not workouts:
        print("\n  No workout data available yet.")
        return
    
    # Calculate various statistics
    total_workouts = len(workouts)
    total_exercises = current_user.get_total_exercises_logged()
    
    # Calculate total volume across all workouts
    # Demonstrates list comprehension and sum()
    total_volume = sum([workout.get_total_volume() for workout in workouts])
    
    # Get date range
    workout_dates = [w.workout_date for w in workouts]
    earliest_workout = min(workout_dates)
    latest_workout = max(workout_dates)
    
    # Calculate workout frequency (workouts per week)
    days_active = (latest_workout - earliest_workout).days + 1
    weeks_active = days_active / 7
    workouts_per_week = total_workouts / weeks_active if weeks_active > 0 else 0
    
    # Find most frequently trained exercises
    # Demonstrates dictionary usage for counting
    exercise_count = {}
    for workout in workouts:
        for we in workout.workout_exercises:
            exercise_name = we.get_exercise_name()
            exercise_count[exercise_name] = exercise_count.get(exercise_name, 0) + 1
    
    # Sort exercises by frequency (most to least)
    # Demonstrates sorted() with dict.items() and lambda
    sorted_exercises = sorted(
        exercise_count.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Display statistics
    print("\n" + "="*60)
    print("  OVERALL STATISTICS")
    print("="*60)
    print(f"\n  Total Workouts: {total_workouts}")
    print(f"  Total Exercises Logged: {total_exercises}")
    print(f"  Total Volume Lifted: {total_volume:,.1f} lbs")
    print(f"\n  First Workout: {earliest_workout}")
    print(f"  Latest Workout: {latest_workout}")
    print(f"  Days Active: {days_active}")
    print(f"  Workout Frequency: {workouts_per_week:.1f} workouts/week")
    
    # Display most trained exercises (top 5)
    print("\n  Most Frequently Trained Exercises:")
    for idx, (exercise_name, count) in enumerate(sorted_exercises[:5], 1):
        print(f"    {idx}. {exercise_name}: {count} sessions")
    
    input("\n  Press Enter to continue...")

# ============================================================================
# EXERCISE LIBRARY FUNCTIONS
# ============================================================================

def search_exercises(session):
    """
    Search for exercises in the library.
    Provides multiple search options: by name, muscle group, or view all.
    
    Args:
        session: SQLAlchemy session
    """
    print_subheader("Search Exercise Library")
    
    print("\n  Search Options:")
    print("  1. Search by name")
    print("  2. Browse by muscle group")
    print("  3. View all exercises")
    print("  0. Cancel")
    
    choice = input("\n  Enter choice: ").strip()
    
    if choice == '1':
        # Search by name
        search_term = input("\n  Enter search term: ").strip()
        if not search_term:
            print("✗ Search term cannot be empty.")
            return
        
        exercises = Exercise.search_by_name(session, search_term)
        display_exercise_list(exercises)
        
    elif choice == '2':
        # Browse by muscle group
        muscle_groups = ('Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core', 'Cardio')
        
        print("\n  Select Muscle Group:")
        for idx, mg in enumerate(muscle_groups, 1):
            print(f"  {idx}. {mg}")
        
        mg_choice = get_valid_integer(
            f"\n  Enter choice (1-{len(muscle_groups)}): ",
            min_value=1,
            max_value=len(muscle_groups)
        )
        
        selected_muscle_group = muscle_groups[mg_choice - 1]
        exercises = Exercise.filter_by_muscle_group(session, selected_muscle_group)
        display_exercise_list(exercises)
        
    elif choice == '3':
        # View all exercises
        exercises = session.query(Exercise).order_by(
            Exercise.muscle_group, Exercise.name
        ).all()
        
        if not exercises:
            print("\n  No exercises in library.")
            return
        
        # Group exercises by muscle group using dictionary
        exercises_by_group = {}
        for exercise in exercises:
            mg = exercise.muscle_group
            if mg not in exercises_by_group:
                exercises_by_group[mg] = []
            exercises_by_group[mg].append(exercise)
        
        # Display grouped exercises
        print(f"\n  Total Exercises: {len(exercises)}\n")
        for muscle_group, exercise_list in exercises_by_group.items():
            print(f"\n  === {muscle_group} ({len(exercise_list)} exercises) ===")
            for exercise in exercise_list:
                print(f"    • {exercise.name}")
                if exercise.equipment_needed:
                    print(f"      Equipment: {exercise.equipment_needed}")
    
    elif choice == '0':
        return
    else:
        print("✗ Invalid choice.")
        return
    
    input("\n  Press Enter to continue...")

def add_custom_exercise(session):
    """
    Add a custom exercise to the library.
    Allows users to add exercises not in the pre-loaded list.
    
    Args:
        session: SQLAlchemy session
    """
    print_subheader("Add Custom Exercise")
    
    # Get exercise details
    name = input("\n  Exercise name: ").strip()
    if not name:
        print("✗ Exercise name cannot be empty.")
        return
    
    # Check if exercise already exists (demonstrates query with filter)
    existing = session.query(Exercise).filter_by(name=name).first()
    if existing:
        print(f"✗ Exercise '{name}' already exists in the library.")
        return
    
    # Select muscle group
    muscle_groups = ('Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core', 'Cardio', 'Other')
    
    print("\n  Select Muscle Group:")
    for idx, mg in enumerate(muscle_groups, 1):
        print(f"  {idx}. {mg}")
    
    mg_choice = get_valid_integer(
        f"\n  Enter choice (1-{len(muscle_groups)}): ",
        min_value=1,
        max_value=len(muscle_groups)
    )
    
    muscle_group = muscle_groups[mg_choice - 1]
    
    # Optional fields
    equipment = input("\n  Equipment needed (optional, press Enter to skip): ").strip()
    equipment = equipment if equipment else None
    
    description = input("  Description (optional, press Enter to skip): ").strip()
    description = description if description else None
    
    # Create new exercise
    new_exercise = Exercise(
        name=name,
        muscle_group=muscle_group,
        equipment_needed=equipment,
        description=description,
        is_custom=True  # Mark as custom exercise
    )
    
    session.add(new_exercise)
    session.commit()
    
    print(f"\n✓ Custom exercise '{name}' added successfully!")

# ============================================================================
# MAIN MENU FUNCTION
# ============================================================================

def main_menu():
    """
    Display main menu and handle user input.
    This is the main loop of the application.
    
    Flow:
        1. Initialize database
        2. Offer to seed if empty
        3. Display menu
        4. Handle user selection
        5. Repeat until user exits
    """
    # Initialize database and seed if needed
    print("Initializing Fitness Tracker...")
    init_db()
    
    # Get database session
    session = get_session()
    
    # Check if database is empty and offer to seed
    exercise_count = session.query(Exercise).count()
    if exercise_count == 0:
        print("\n! Exercise library is empty.")
        if confirm_action("Would you like to populate it with default exercises?"):
            seed_database()
    
    # Main application loop
    while True:
        # Display header
        print_header("FITNESS TRACKER & WORKOUT PLANNER")
        
        # Display current user status
        if current_user:
            print(f"\n  Current User: {current_user.name}")
            print(f"  Workouts Logged: {current_user.get_workout_count()}")
        else:
            print("\n  No user selected - Please create or select a user")
        
        # Display menu options
        print("\n  MAIN MENU:")
        print("  1. User Management (Create/Switch User)")
        print("  2. Log New Workout")
        print("  3. View Workout History")
        print("  4. View Exercise History")
        print("  5. View Statistics")
        print("  6. Search Exercise Library")
        print("  7. Add Custom Exercise")
        print("  0. Exit")
        
        # Get user choice
        choice = input("\n  Enter your choice: ").strip()
        
        # Handle menu selection
        if choice == '1':
            user_management_menu(session)
        elif choice == '2':
            log_workout(session)
        elif choice == '3':
            view_workout_history(session)
        elif choice == '4':
            view_exercise_history(session)
        elif choice == '5':
            view_statistics(session)
        elif choice == '6':
            search_exercises(session)
        elif choice == '7':
            add_custom_exercise(session)
        elif choice == '0':
            # Exit application
            print("\n" + "="*60)
            print("  Thank you for using Fitness Tracker!")
            print("  Keep pushing your limits! ")
            print("="*60 + "\n")
            session.close()
            sys.exit(0)
        else:
            print("\n✗ Invalid choice. Please enter a number from the menu.")
        
        # Pause before showing menu again
        input("\n  Press Enter to return to main menu...")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Entry point for the Fitness Tracker CLI application.
    Run this file to start the application: python lib/cli.py
    
    Handles:
        - Normal execution flow
        - Keyboard interrupt (Ctrl+C)
        - Unexpected errors
    """
    try:
        main_menu()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n  Application interrupted by user. Goodbye! 👋\n")
        sys.exit(0)
    except Exception as e:
        # Handle unexpected errors
        print(f"\n✗ An error occurred: {e}")
        print("  Please report this issue if it persists.\n")
        sys.exit(1)

