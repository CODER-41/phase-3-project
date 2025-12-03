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