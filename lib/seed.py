"""
Seed data for Fitness Tracker Application.
Populates the database with common exercises organized by muscle group.
"""

from lib.database import get_session, init_db
from lib.models import Exercise, User, Workout, WorkoutExercise  # Fixed: EXercise -> Exercise
from datetime import date, timedelta

# Tuple of muscle groups (immutable - these are the standard categories)
MUSCLE_GROUPS = ('Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core', 'Cardio')  # Fixed: 'chest' -> 'Chest'

# Dictionary mapping muscle groups to exercises
# This demonstrates use of dict data structure
EXERCISE_DATA = {
    'Chest': [
        {'name': 'Bench Press', 'equipment': 'Barbell', 'description': 'Compound chest exercise'},
        {'name': 'Incline Bench Press', 'equipment': 'Barbell', 'description': 'Upper chest focus'},
        {'name': 'Dumbbell Bench Press', 'equipment': 'Dumbbells', 'description': 'Chest exercise with dumbbells'},
        {'name': 'Dumbbell Flyes', 'equipment': 'Dumbbells', 'description': 'Chest isolation exercise'},
        {'name': 'Push-ups', 'equipment': 'Bodyweight', 'description': 'Bodyweight chest exercise'},
        {'name': 'Cable Flyes', 'equipment': 'Cable Machine', 'description': 'Cable chest isolation'},
    ],
    'Back': [
        {'name': 'Deadlift', 'equipment': 'Barbell', 'description': 'Full body compound movement'},
        {'name': 'Barbell Row', 'equipment': 'Barbell', 'description': 'Back thickness builder'},
        {'name': 'Pull-ups', 'equipment': 'Bodyweight', 'description': 'Bodyweight back exercise'},
        {'name': 'Lat Pulldown', 'equipment': 'Cable Machine', 'description': 'Lat width builder'},
        {'name': 'Dumbbell Row', 'equipment': 'Dumbbells', 'description': 'Unilateral back exercise'},
        {'name': 'Seated Cable Row', 'equipment': 'Cable Machine', 'description': 'Mid-back exercise'},
    ],
    'Legs': [
        {'name': 'Squat', 'equipment': 'Barbell', 'description': 'Compound leg exercise'},
        {'name': 'Front Squat', 'equipment': 'Barbell', 'description': 'Quad-focused squat variation'},
        {'name': 'Leg Press', 'equipment': 'Machine', 'description': 'Machine-based leg exercise'},
        {'name': 'Leg Curl', 'equipment': 'Machine', 'description': 'Hamstring isolation'},
        {'name': 'Leg Extension', 'equipment': 'Machine', 'description': 'Quad isolation'},
        {'name': 'Lunges', 'equipment': 'Dumbbells', 'description': 'Unilateral leg exercise'},
        {'name': 'Romanian Deadlift', 'equipment': 'Barbell', 'description': 'Hamstring and glute focus'},
    ],
    'Shoulders': [
        {'name': 'Overhead Press', 'equipment': 'Barbell', 'description': 'Compound shoulder exercise'},
        {'name': 'Dumbbell Shoulder Press', 'equipment': 'Dumbbells', 'description': 'Shoulder press variation'},
        {'name': 'Lateral Raises', 'equipment': 'Dumbbells', 'description': 'Side delt isolation'},
        {'name': 'Front Raises', 'equipment': 'Dumbbells', 'description': 'Front delt isolation'},
        {'name': 'Face Pulls', 'equipment': 'Cable Machine', 'description': 'Rear delt and upper back'},
    ],
    'Arms': [
        {'name': 'Barbell Curl', 'equipment': 'Barbell', 'description': 'Bicep mass builder'},
        {'name': 'Dumbbell Curl', 'equipment': 'Dumbbells', 'description': 'Bicep exercise'},
        {'name': 'Hammer Curl', 'equipment': 'Dumbbells', 'description': 'Bicep and forearm exercise'},
        {'name': 'Tricep Pushdown', 'equipment': 'Cable Machine', 'description': 'Tricep isolation'},
        {'name': 'Skull Crushers', 'equipment': 'Barbell', 'description': 'Tricep extension'},
        {'name': 'Close-Grip Bench Press', 'equipment': 'Barbell', 'description': 'Compound tricep exercise'},
    ],
    'Core': [
        {'name': 'Plank', 'equipment': 'Bodyweight', 'description': 'Core stability exercise'},
        {'name': 'Crunches', 'equipment': 'Bodyweight', 'description': 'Abdominal exercise'},
        {'name': 'Russian Twists', 'equipment': 'Bodyweight', 'description': 'Oblique exercise'},
        {'name': 'Hanging Leg Raises', 'equipment': 'Pull-up Bar', 'description': 'Lower ab exercise'},
        {'name': 'Cable Crunches', 'equipment': 'Cable Machine', 'description': 'Weighted ab exercise'},
    ],
    'Cardio': [
        {'name': 'Running', 'equipment': 'None', 'description': 'Cardiovascular exercise'},
        {'name': 'Cycling', 'equipment': 'Bike', 'description': 'Low-impact cardio'},
        {'name': 'Rowing', 'equipment': 'Rowing Machine', 'description': 'Full body cardio'},
        {'name': 'Jump Rope', 'equipment': 'Jump Rope', 'description': 'High-intensity cardio'},
    ],
}

def seed_exercises(session):
    """
    Populate the database with pre-defined exercises.
    Only runs if exercises table is empty.
    
    Args:
        session: SQLAlchemy session
    """
    # Check if exercises already exist
    existing_count = session.query(Exercise).count()
    if existing_count > 0:
        print(f"✓ Exercise library already populated ({existing_count} exercises)")
        return
    
    print("Seeding exercise library...")
    
    # Counter for tracking inserted exercises
    total_exercises = 0  # Fixed: total_exercise -> total_exercises
    
    # Iterate through the dictionary of exercises by muscle group
    for muscle_group, exercises_list in EXERCISE_DATA.items():
        # exercises_list is a list of dictionaries
        for exercise_dict in exercises_list:
            # Create new Exercise object
            exercise = Exercise(
                name=exercise_dict['name'],
                muscle_group=muscle_group,
                equipment_needed=exercise_dict['equipment'],
                description=exercise_dict['description'],
                is_custom=False  # Pre-loaded exercises
            )
            session.add(exercise)
            total_exercises += 1
    
    # Commit all exercises to database
    session.commit()
    print(f"✓ Seeded {total_exercises} exercises across {len(MUSCLE_GROUPS)} muscle groups")


def seed_sample_user_custom_name(session):
    """
    Create a sample user with a CUSTOM NAME.
    
    Args:
        session: SQLAlchemy session
    """
    # Your custom information
    custom_name = "Ronny Mboya"
    custom_age = 43
    custom_weight = 175.0
    custom_goal = "Get stronger and build lean muscle"
    
    # Check if user already exists (by name)
    existing_user = session.query(User).filter_by(name=custom_name).first()
    if existing_user:
        print(f"✓ User '{custom_name}' already exists")
        return
    
    print(f"Creating sample user '{custom_name}' with demo workouts...")
    
    # Create the user with your custom name
    demo_user = User(
        name=custom_name,
        age=custom_age,
        weight=custom_weight,
        fitness_goal=custom_goal
    )
    session.add(demo_user)
    session.commit()
    
    # Get some exercises for demo workouts
    bench_press = session.query(Exercise).filter_by(name="Bench Press").first()
    squat = session.query(Exercise).filter_by(name="Squat").first()
    deadlift = session.query(Exercise).filter_by(name="Deadlift").first()
    
    if not (bench_press and squat and deadlift):
        print("! Could not create demo workouts - exercises not found")
        return
    
    # Create sample workout 1 (3 days ago) - Chest Day
    workout1 = Workout(
        user=demo_user,
        workout_date=date.today() - timedelta(days=3),
        notes="Great chest day! Felt really strong on bench press."
    )
    session.add(workout1)
    
    # Add exercises to workout 1
    we1 = WorkoutExercise(
        workout=workout1,
        exercise=bench_press,
        sets=3,
        reps=10,
        weight=135.0,
        notes="Added 5 lbs from last session"
    )
    session.add(we1)
    
    # Create sample workout 2 (1 day ago) - Leg Day
    workout2 = Workout(
        user=demo_user,
        workout_date=date.today() - timedelta(days=1),
        notes="Leg day - tough but productive"
    )
    session.add(workout2)
    
    # Add exercises to workout 2
    we2 = WorkoutExercise(
        workout=workout2,
        exercise=squat,
        sets=4,
        reps=8,
        weight=225.0,
        notes="New PR!"
    )
    we3 = WorkoutExercise(
        workout=workout2,
        exercise=deadlift,
        sets=3,
        reps=5,
        weight=275.0,
        notes="Form felt solid"
    )
    session.add(we2)
    session.add(we3)
    
    session.commit()
    print(f"✓ Created user '{demo_user.name}' with 2 sample workouts")


def seed_multiple_demo_users(session):
    """
    Create MULTIPLE sample users to show variety.
    
    Args:
        session: SQLAlchemy session
    """
    # List of demo users with different profiles (demonstrates use of list)
    demo_users_data = [
        {
            'name': 'Sarah Johnson',
            'age': 24,
            'weight': 140.0,
            'goal': 'Lose weight and tone up'
        },
        {
            'name': 'Mike Thompson',
            'age': 35,
            'weight': 200.0,
            'goal': 'Build muscle mass'
        },
        {
            'name': 'Omar Lisa',
            'age': 29,
            'weight': 130.0,
            'goal': 'Improve overall fitness'
        }
    ]
    
    print(f"Creating {len(demo_users_data)} sample users...")
    
    for user_data in demo_users_data:
        # Check if user already exists
        existing = session.query(User).filter_by(name=user_data['name']).first()
        if existing:
            print(f"✓ User '{user_data['name']}' already exists")
            continue
        
        # Create new user
        new_user = User(
            name=user_data['name'],
            age=user_data['age'],
            weight=user_data['weight'],
            fitness_goal=user_data['goal']
        )
        session.add(new_user)
        print(f"  • Created user: {user_data['name']}")
    
    session.commit()
    print(f"✓ Multiple demo users created successfully")


def seed_no_demo_user(session):
    """
    Don't create any demo users.
    Use this if you want a completely empty database.
    
    Args:
        session: SQLAlchemy session
    """
    print("✓ Skipping demo user creation - database will be empty")
    print("  Users can create their own accounts from the CLI")
    # This function intentionally does nothing - just for clarity


def seed_database():
    """
    Main seeding function - initializes database and populates with data.
    """
    # Initialize database tables
    init_db()
    
    # Get database session
    session = get_session()
    
    try:
        # ALWAYS seed exercises (required for app to work)
        seed_exercises(session)
        
        # Create demo user with your name
        seed_sample_user_custom_name(session)
        
        # Optional: Create multiple demo users (commented out)
        # seed_multiple_demo_users(session)
        
        # Optional: Skip demo user creation (commented out)
        # seed_no_demo_user(session)
        
        print("\n" + "="*60)
        print("DATABASE SEEDING COMPLETE!")
        print("="*60)
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        session.rollback()
    finally:
        session.close()


# Run seeding if this file is executed directly
if __name__ == "__main__":
    seed_database()