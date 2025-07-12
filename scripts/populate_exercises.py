#!/usr/bin/env python3
"""
Script to populate the database with sample exercises
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.crud.exercise import create_exercise
from app.schemas.exercise import ExerciseCreate

def populate_exercises():
    """Populate database with sample exercises"""
    db = SessionLocal()
    
    sample_exercises = [
        {
            "name": "Dumbbell Press",
            "description": "Chest exercise using dumbbells for strength and muscle building"
        },
        {
            "name": "Squats",
            "description": "Lower body exercise targeting quadriceps, hamstrings, and glutes"
        },
        {
            "name": "Deadlift",
            "description": "Compound exercise for back, legs, and core strength"
        },
        {
            "name": "Bench Press",
            "description": "Classic chest exercise using barbell"
        },
        {
            "name": "Pull-ups",
            "description": "Upper body exercise targeting back and biceps"
        },
        {
            "name": "Push-ups",
            "description": "Bodyweight exercise for chest, shoulders, and triceps"
        },
        {
            "name": "Lunges",
            "description": "Lower body exercise for balance and leg strength"
        },
        {
            "name": "Plank",
            "description": "Core exercise for stability and strength"
        },
        {
            "name": "Bicep Curls",
            "description": "Isolation exercise for bicep development"
        },
        {
            "name": "Tricep Dips",
            "description": "Upper body exercise targeting triceps"
        },
        {
            "name": "Shoulder Press",
            "description": "Overhead press for shoulder strength"
        },
        {
            "name": "Leg Press",
            "description": "Machine-based leg exercise"
        },
        {
            "name": "Lat Pulldown",
            "description": "Back exercise using cable machine"
        },
        {
            "name": "Chest Flyes",
            "description": "Isolation exercise for chest muscles"
        },
        {
            "name": "Leg Extensions",
            "description": "Isolation exercise for quadriceps"
        }
    ]
    
    try:
        for exercise_data in sample_exercises:
            exercise = ExerciseCreate(**exercise_data)
            created_exercise = create_exercise(db, exercise)
            print(f"Created exercise: {created_exercise.name} (ID: {created_exercise.id})")
        
        print(f"\nSuccessfully created {len(sample_exercises)} exercises!")
        
    except Exception as e:
        print(f"Error creating exercises: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Populating database with sample exercises...")
    populate_exercises() 