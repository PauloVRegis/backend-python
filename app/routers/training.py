from fastapi import APIRouter, Depends, HTTPException, Body, Query, Path, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..schemas.training import TrainingCreate, Training, TrainingResponse
from ..crud.training import create_training, get_training, get_trainings_by_user, get_trainings_by_professor, get_training_with_exercises
from ..crud.user import get_user
from ..middleware.auth import get_current_active_user, rate_limit
from ..utils.cache import cache_training_data, cache_service
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/trainings/", response_model=TrainingResponse)
async def create_new_training(
    request: Request,
    training: TrainingCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new training session"""
    try:
        # Validate user exists
        user = get_user(db, user_id=training.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate professor exists
        professor = get_user(db, user_id=training.professor_id)
        if professor is None:
            raise HTTPException(status_code=404, detail="Professor not found")
        
        # Create training
        new_training = create_training(
            db=db, 
            training=training, 
            user_id=training.user_id, 
            professor_id=training.professor_id
        )
        
        # Invalidate related caches
        await cache_service.delete_pattern(f"training:user:{training.user_id}:*")
        await cache_service.delete_pattern(f"training:professor:{training.professor_id}:*")
        
        logger.info(f"Training created: {new_training.id} by user {current_user['user_id']}")
        return new_training
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating training: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/trainings/{training_id}", response_model=TrainingResponse)
async def get_training_by_id(
    training_id: int = Path(..., description="Training ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get training by ID"""
    try:
        training = get_training_with_exercises(db, training_id=training_id)
        if training is None:
            raise HTTPException(status_code=404, detail="Training not found")
        
        # Check if user has access to this training
        if str(training.user_id) != current_user['user_id'] and str(training.professor_id) != current_user['user_id']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return training
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving training {training_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/trainings/{training_id}/description")
async def get_training_description(
    training_id: int = Path(..., description="Training ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get training description"""
    try:
        training = get_training(db, training_id=training_id)
        if training is None:
            raise HTTPException(status_code=404, detail="Training not found")
        
        # Check access
        if str(training.user_id) != current_user['user_id'] and str(training.professor_id) != current_user['user_id']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return {"description": training.description}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving training description {training_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/trainings/user/{user_id}", response_model=List[TrainingResponse])
async def get_user_trainings(
    user_id: int = Path(..., description="User ID"),
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all trainings for a specific user"""
    try:
        # Check if current user can access this user's trainings
        if str(user_id) != current_user['user_id']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        trainings = get_trainings_by_user(db, user_id=user_id, skip=skip, limit=limit)
        return trainings
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving trainings for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/trainings/professor/{professor_id}", response_model=List[TrainingResponse])
async def get_professor_trainings(
    professor_id: int = Path(..., description="Professor ID"),
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all trainings created by a specific professor"""
    try:
        # Check if current user can access this professor's trainings
        if str(professor_id) != current_user['user_id']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        trainings = get_trainings_by_professor(db, professor_id=professor_id, skip=skip, limit=limit)
        return trainings
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving trainings for professor {professor_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/trainings/{training_id}", response_model=TrainingResponse)
async def update_training(
    request: Request,
    training_id: int = Path(..., description="Training ID"),
    training_update: TrainingCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Update an existing training"""
    try:
        # Get existing training
        existing_training = get_training(db, training_id=training_id)
        if existing_training is None:
            raise HTTPException(status_code=404, detail="Training not found")
        
        # Check if user can update this training
        if str(existing_training.professor_id) != current_user['user_id']:
            raise HTTPException(status_code=403, detail="Only the professor can update this training")
        
        # Update training (implement update logic in CRUD)
        # For now, return existing training
        # TODO: Implement actual update logic
        
        # Invalidate caches
        await cache_service.delete_pattern(f"training:*")
        
        logger.info(f"Training updated: {training_id} by user {current_user['user_id']}")
        return existing_training
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating training {training_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/trainings/{training_id}")
async def delete_training(
    request: Request,
    training_id: int = Path(..., description="Training ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a training"""
    try:
        # Get existing training
        existing_training = get_training(db, training_id=training_id)
        if existing_training is None:
            raise HTTPException(status_code=404, detail="Training not found")
        
        # Check if user can delete this training
        if str(existing_training.professor_id) != current_user['user_id']:
            raise HTTPException(status_code=403, detail="Only the professor can delete this training")
        
        # Delete training (implement delete logic in CRUD)
        # For now, return success message
        # TODO: Implement actual delete logic
        
        # Invalidate caches
        await cache_service.delete_pattern(f"training:*")
        
        logger.info(f"Training deleted: {training_id} by user {current_user['user_id']}")
        return {"message": "Training deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting training {training_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")