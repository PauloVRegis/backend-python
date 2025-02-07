from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    professor_id: int

class User(UserBase):
    id: int
    professor_id: int

    class Config:
        orm_mode = True