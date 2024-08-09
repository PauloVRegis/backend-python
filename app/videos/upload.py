# Upload videos from student to teacher and  store vide in /app/videos/storage/student_id/teacher_id/video_id.mp4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.models import Video
from app.api.models import Student
from app.api.models import Teacher
from datetime import datetime

router = APIRouter()

@router.post("/videos/")
def create_video(student_id: int, teacher_id: int, file_path: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    video = Video(student_id=student_id, teacher_id=teacher_id, file_path=file_path)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video



