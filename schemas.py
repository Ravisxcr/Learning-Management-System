from pydantic import BaseModel, EmailStr
from typing import List
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: str


class Roles(str, Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"

class Level(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'

class EmailSchema(BaseModel):
    email: List[EmailStr]

class Login(BaseModel):
    username : str
    password : str

class Registration(BaseModel):
    username :str
    password : str
    role : Roles

class Student(BaseModel):
    Sid : str
    Roll_no : int
    Sname : str
    Class : int
    Age : int
    Address : str
    Email_home : str 
    Phone : int

class TeacherDet(BaseModel):
    Tid : int
    Tname : str
    Designation : str
    Age : int
    Address : str 
    Email_office : str 
    Email_home : str
    Phone : int

class SubList(BaseModel):
    Sub_id : str
    Sub_name : str
    Faculty_id : str
    Course_credit : int
    Course_level : Level

class StudentMarks(BaseModel):
    sid : str
    subid : str
    score : int
    remarks : str

class DeleteID(BaseModel):
    id : str
    