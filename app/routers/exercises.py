from fastapi import APIRouter, Depends, HTTPException, Body, Query, Path, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..schemas.exercise import ExerciseCreate, Exercise
from ..crud.exercise import create_exercise, get_exercise, get_exercises, get_exercises_by_name, update_exercise, delete_exercise
from ..middleware.auth import get_current_active_user, rate_limit
from ..utils.cache import cache_service
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/exercises/", response_model=Exercise)
async def create_new_exercise(
    request: Request,
    exercise: ExerciseCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new exercise in the catalog"""
    try:
        # Only professors can create exercises
        # You might want to add role checking here
        new_exercise = create_exercise(db, exercise)
        
        # Invalidate exercise cache
        await cache_service.delete_pattern("exercise:*")
        
        logger.info(f"Exercise created: {new_exercise.id} by user {current_user['user_id']}")
        return new_exercise
        
    except Exception as e:
        logger.error(f"Error creating exercise: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/exercises/", response_model=List[Exercise])
async def get_exercise_catalog(
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    name: Optional[str] = Query(None, description="Filter by exercise name"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get exercise catalog with optional filtering"""
    try:
        if name:
            exercises = get_exercises_by_name(db, name, skip=skip, limit=limit)
        else:
            exercises = get_exercises(db, skip=skip, limit=limit)
        
        return exercises
        
    except Exception as e:
        logger.error(f"Error retrieving exercises: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/exercises/{exercise_id}", response_model=Exercise)
async def get_exercise_by_id(
    exercise_id: int = Path(..., description="Exercise ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get exercise by ID"""
    try:
        exercise = get_exercise(db, exercise_id)
        if exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        return exercise
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving exercise {exercise_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/exercises/{exercise_id}", response_model=Exercise)
async def update_exercise_by_id(
    request: Request,
    exercise_id: int = Path(..., description="Exercise ID"),
    exercise_update: ExerciseCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Update an existing exercise"""
    try:
        # Check if exercise exists
        existing_exercise = get_exercise(db, exercise_id)
        if existing_exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        # Update exercise
        updated_exercise = update_exercise(db, exercise_id, exercise_update)
        
        # Invalidate cache
        await cache_service.delete_pattern("exercise:*")
        
        logger.info(f"Exercise updated: {exercise_id} by user {current_user['user_id']}")
        return updated_exercise
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating exercise {exercise_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/exercises/{exercise_id}")
async def delete_exercise_by_id(
    request: Request,
    exercise_id: int = Path(..., description="Exercise ID"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Delete an exercise"""
    try:
        # Check if exercise exists
        existing_exercise = get_exercise(db, exercise_id)
        if existing_exercise is None:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        # Delete exercise
        success = delete_exercise(db, exercise_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete exercise")
        
        # Invalidate cache
        await cache_service.delete_pattern("exercise:*")
        
        logger.info(f"Exercise deleted: {exercise_id} by user {current_user['user_id']}")
        return {"message": "Exercise deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting exercise {exercise_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 