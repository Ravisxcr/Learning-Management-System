from fastapi import FastAPI, Request, APIRouter,Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from fastapi.responses import HTMLResponse


from database import *
import database as db
from schemas import *
import authentication_fun as au

app = FastAPI()
app.secret = None
app.data = None

oth2_scheme = OAuth2PasswordBearer(tokenUrl='token')



@app.post('/token')
async def generate_token(request_form : OAuth2PasswordRequestForm = Depends()):
    print((request_form.username, request_form.password))
    r = db.authenticate_login(request_form.username, request_form.password)
    if r is not None:
        return r
    else:
        raise HTTPException(status_code=400, detail="incorrect info")


@app.get("/")
def home(token: str=Depends(oth2_scheme)):
    if app.data:
        return au.very_token(app.data)
    return dict(app.data)



@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.get("/ping/data")
async def ping():
    return app.data

@app.get("/student")
async def get_student_details():
    return db.all_student_deatils()

@app.post("/registration")
async def login_registration(user: Registration, token: str=Depends(oth2_scheme)):
    user_info = dict(user)
    user_info['password'] = au.get_hash_password(user_info['password'])
    return db.create_login(user_info['username'], user_info['password'], user_info["role"])

@app.post("/login")
async def login(user: Login):
    user_info = dict(user)
    r = db.authenticate_login(user.username, user.password)
    if r :
        app.secret = r
        app.data = au.create_access_token(user,r)
        return user_info
    else:
        raise HTTPException(status_code=400, detail="incorrect info")

    

@app.post('/admission')
async def new_admission_form(request : Student, token: str=Depends(oth2_scheme)):
    if app.secret and app.secret == "admin":
        stu_info = dict(request)
        return admission(stu_info)
    else:
        return {"message": "you are not admin"}


@app.get("/teacher")
async def get_teacher_details():   
    if app.secret and app.secret == "admin":
        return db.teacher_deatils()
    else:
        return {"message": "you are not admin"}
    

@app.get("/sublist")
async def get_sublist():
    return db.subject_list()

@app.post('/newfaculty')
async def new_faculty(request : Teacher, token: str=Depends(oth2_scheme)):
    teach_info = dict(request)
    return new_teacher(teach_info)

@app.delete('/delstudent')
async def remove_student(request : Studentdel, token: str=Depends(oth2_scheme)):
    User.query.filter_by(id=123).delete()
    return request



if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
