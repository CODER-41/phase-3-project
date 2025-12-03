from lib.database import get_session, init_db
from lib.models import EXercise, User, Workout, WorkoutExercise
from datetime import date, timedelta

MUSCLE_GROUPS = ('chest', 'Back', 'Legs', 'Shoulders','Arms', 'Core', 'Cardio')

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
    existing_count = session.query(Exercise).count()
    if existing_count > 0:
        print(f"Exercise library already populated ({existing_count} exercises)")
        return 
    
    print("Seeding exercise library...")

    total_exercise = 0

    for muscle_group, exercise_list in EXERCISE_DATA.items():
        for exercise_dict in exercise_list:
            exercise = Exercise(
                name = exercise_dict['name'],
                muscle_group = muscle_group,
                equipment_needed = exercise_dict['equipment'],
                description = exercise_dict['description'],
                is_custom = False
            )
            session.add(exercise)
            total_exercises += 1

        session.commit()
        print(f"Seeded {total_exercise} exercises across {len(MUSCLE_GROUPS)} muscle groups")
