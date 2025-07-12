from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..schemas.professor import Professor, ProfessorCreate
from ..crud.professor import get_professor, create_professor, get_professors
from ..database.session import get_db
from ..middleware.auth import get_current_active_user
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/professors/", response_model=List[Professor])
async def list_professors(
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all professors with pagination"""
    try:
        professors = get_professors(db, skip=skip, limit=limit)
        return professors
    except Exception as e:
        logger.error(f"Error retrieving professors: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/professors/{professor_id}", response_model=Professor)
async def read_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get professor by ID"""
    try:
        professor = get_professor(db, professor_id)
        if professor is None:
            raise HTTPException(status_code=404, detail="Professor not found")
        return professor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving professor {professor_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/professors/", response_model=Professor)
async def create_new_professor(
    professor: ProfessorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new professor"""
    try:
        return create_professor(db=db, professor=professor)
    except Exception as e:
        logger.error(f"Error creating professor: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")