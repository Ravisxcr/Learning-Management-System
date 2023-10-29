from fastapi import FastAPI, Request, APIRouter,Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from fastapi.responses import HTMLResponse


from database import *
import database as db
from schemas import *
from authentication import *

app = FastAPI()

oth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/token')
async def generate_token(request_form : OAuth2PasswordRequestForm = Depends()):
    print((request_form.username, request_form.password))
    if authenticate_login(request_form.username, request_form.password):
        return {"access_token" : 'token', "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="incorernt info")


@app.get("/")
def home(token: str=Depends(oth2_scheme)):
    return {"token": token}



@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.get("/student")
async def get_student_details():
    return db.student_deatils()

@app.post("/registration")
async def login_registration(user: Registration):
    user_info = dict(user)
    user_info['password'] = get_hash_password(user_info['password'])
    return create_login(user_info['username'], user_info['password'])
    

@app.post('/admission')
async def new_admission_form(request : Student):
    stu_info = dict(request)
    return admission(stu_info)


@app.get("/teacher")
async def get_teacher_details():
    return db.teacher_deatils()

@app.get("/sublist")
async def get_sublist():
    return db.subject_list()

@app.post('/newfaculty')
async def new_faculty(request : Teacher):
    teach_info = dict(request)
    return new_teacher(teach_info)

@app.delete('/delstudent')
async def remove_student(request : Studentdel):
    return request

@app.post('/login')
async def login(request : Login):
    ref = get_hash_password(request.password)
    db.create_login(request.username,ref)
    return request


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
