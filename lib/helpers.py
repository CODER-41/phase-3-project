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