#!/usr/bin/env python3
"""
Script to recreate the database with the new schema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.database.session import Base, engine
from app.models.user import User
from app.models.professor import Professor
from app.models.training import Training, TrainingExercise
from app.models.exercise import Exercise
from app.models.training_logical import TrainingRegistration

def recreate_database():
    """Recreate the database with new schema"""
    print("🗄️ Recreating database with new schema...")
    
    try:
        # Drop all tables
        print("📥 Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        # Create all tables with new schema
        print("📤 Creating new tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database recreated successfully!")
        print("📋 New schema includes:")
        print("   - users (id, email, name, password_hash, created_at)")
        print("   - professors (id, name, created_at)")
        print("   - exercises (id, name, description, created_at)")
        print("   - trainings (id, name, description, user_id, professor_id, created_at)")
        print("   - training_exercises (id, training_id, exercise_id, sets, repetitions)")
        print("   - training_registration (id, training_id, exercise_id, user_id, professor_id, repetitions, load, sets, volume, intensity, created_at)")
        
    except Exception as e:
        print(f"❌ Error recreating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    recreate_database() 