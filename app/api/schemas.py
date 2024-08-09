from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    user_id: int

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    user: UserOut
    videos: List['VideoOut'] = []

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    user_id: int

class TeacherCreate(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    id: int
    user: UserOut
    videos: List['VideoOut'] = []

    class Config:
        orm_mode = True

class VideoBase(BaseModel):
    student_id: int
    teacher_id: int
    file_path: str

class VideoCreate(VideoBase):
    pass

class VideoOut(VideoBase):
    id: int
    upload_time: datetime

    class Config:
        orm_mode = True
