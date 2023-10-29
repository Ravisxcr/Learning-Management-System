from pydantic import BaseModel, EmailStr
from typing import List
from enum import Enum

class Roles(str, Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"

class EmailSchema(BaseModel):
    email: List[EmailStr]

class Login(BaseModel):
    username : str
    password : str

class Registration(BaseModel):
    username :str
    password : str
    role : Roles = "student"

class Student(BaseModel):
    Sid : str
    Roll_no : int
    Sname : str
    Class : int
    Age : int
    Address : str
    Email_home : str 
    Phone : int

class Teacher(BaseModel):
    Tid : int
    Tname : str
    Designation : str
    Age : int
    Address : str 
    Email_office : str 
    Email_home : str
    Phone : int

class Sublist(BaseModel):
    Sub_id : str
    Sub_name : str
    Faculty_id : int
    Slot : str

class Studentdel(BaseModel):
    Sid : str
    Roll_no : int
    Sname : str