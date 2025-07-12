#!/usr/bin/env python3
"""
Script to populate the database with sample professors
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.professor import Professor

def populate_professors():
    """Populate database with sample professors"""
    db = SessionLocal()
    
    sample_professors = [
        {
            "name": "João Silva",
        },
        {
            "name": "Maria Santos",
        },
        {
            "name": "Carlos Oliveira",
        },
        {
            "name": "Ana Costa",
        },
        {
            "name": "Pedro Ferreira",
        }
    ]
    
    try:
        for professor_data in sample_professors:
            # Check if professor already exists
            existing = db.query(Professor).filter(Professor.name == professor_data["name"]).first()
            if not existing:
                professor = Professor(**professor_data)
                db.add(professor)
                db.flush()  # Get the ID
                print(f"Created professor: {professor.name} (ID: {professor.id})")
            else:
                print(f"Professor already exists: {professor_data['name']} (ID: {existing.id})")
        
        db.commit()
        print(f"\nSuccessfully processed {len(sample_professors)} professors!")
        
    except Exception as e:
        print(f"Error creating professors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Populating database with sample professors...")
    populate_professors() 