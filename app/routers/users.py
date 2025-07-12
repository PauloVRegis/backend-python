from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..schemas.user import User, UserCreate
from ..crud.user import get_user, create_user, get_users
from ..database.session import get_db
from ..middleware.auth import get_current_active_user
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/users/", response_model=List[User])
async def list_users(
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get all users with pagination"""
    try:
        users = get_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/users/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get user by ID"""
    try:
        user = get_user(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Test endpoint without auth to isolate the issue
@router.get("/users/test/{user_id}", response_model=User)
async def test_read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Test endpoint without auth"""
    try:
        user = get_user(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/users/", response_model=User)
async def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new user"""
    try:
        return create_user(db=db, user=user)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")