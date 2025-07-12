from sqlalchemy.orm import Session
from ..models.training import Training, TrainingExercise
from ..schemas.training import TrainingCreate
from ..models.user import User
from ..models.professor import Professor
from ..models.exercise import Exercise

def create_training(db: Session, training: TrainingCreate, user_id: int, professor_id: int):
    """Create training with exercises"""
    # Validate user and professor exist
    user = db.query(User).filter(User.id == user_id).first()
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    
    if not user:
        raise ValueError("User not found")
    if not professor:
        raise ValueError("Professor not found")
    
    # Create training
    training_data = training.model_dump(exclude={'exercises'})
    db_training = Training(**training_data)
    db_training.user_id = user_id
    db_training.professor_id = professor_id
    db.add(db_training)
    db.flush()  # Get the training ID
    
    # Add exercises to training
    for exercise_data in training.exercises:
        # Validate exercise exists
        exercise = db.query(Exercise).filter(Exercise.id == exercise_data.exercise_id).first()
        if not exercise:
            raise ValueError(f"Exercise with ID {exercise_data.exercise_id} not found")
        
        # Create training exercise
        db_training_exercise = TrainingExercise(
            training_id=db_training.id,
            exercise_id=exercise_data.exercise_id,
            sets=exercise_data.sets,
            repetitions=exercise_data.repetitions
        )
        db.add(db_training_exercise)
    
    db.commit()
    db.refresh(db_training)
    return db_training

def get_training(db: Session, training_id: int):
    """Get training by ID with exercises"""
    return db.query(Training).filter(Training.id == training_id).first()

def get_trainings_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all trainings for a specific user"""
    return db.query(Training).filter(Training.user_id == user_id).offset(skip).limit(limit).all()

def get_trainings_by_professor(db: Session, professor_id: int, skip: int = 0, limit: int = 100):
    """Get all trainings created by a specific professor"""
    return db.query(Training).filter(Training.professor_id == professor_id).offset(skip).limit(limit).all()

def get_training_with_exercises(db: Session, training_id: int):
    """Get training with detailed exercise information"""
    training = db.query(Training).filter(Training.id == training_id).first()
    if training:
        # Load exercises with details
        for training_exercise in training.training_exercises:
            exercise = db.query(Exercise).filter(Exercise.id == training_exercise.exercise_id).first()
            if exercise:
                training_exercise.exercise_name = exercise.name
                training_exercise.exercise_description = exercise.description
    return training