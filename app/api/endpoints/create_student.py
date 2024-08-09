# Endpoint to create a student
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.models import Student

router = APIRouter()

@router.post("/students/")
def create_student(first_name: str, last_name: str, db: Session = Depends(get_db)):
    student = Student(first_name=first_name, last_name=last_name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

# Create relationships between student to teacher

def create_student_teacher_relationship(student_id: int, teacher_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    student.teachers.append(teacher)
    db.commit()
    db.refresh(student)
    return student



