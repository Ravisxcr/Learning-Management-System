from fastapi import FastAPI,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
import uvicorn
from datetime import timedelta
from database import *
import database as db
from schemas import *
from authentication import *

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(debug=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str  = payload.get("role")
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    return token_data


@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.get("/my_status")
async def my_status(current_user: TokenData = Depends(get_current_user)):
    try:
        return current_user
    except:
        return "Error occured"


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": form_data.username}, role=user, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


    
@app.post("/registration")
async def login_registration(user: Registration, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user.role == "admin":
            return db.create_login(user)
        else:
            return {"message": "you are not admin"}     
    except Exception as ex:
        print(str(ex))
        raise ex

@app.get("/student")
async def get_student_details(current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user.role == "admin":
            return db.all_student_deatils()
        else:
            return {"message": "you are not admin"}
    except:
        return "Error occured"
    

@app.get("/my_marks")
async def get_student_details(current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user.role == "student":
            return get_my_marks(current_user.username)
        else:
            return {"message": "you are not student"}
    except:
        return "Error occured"



@app.post('/admission')
async def new_admission_form(request : Union[Student, List], current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user.role == "admin":
            stu_info = dict(request)
            return admission(stu_info)
        else:
            return {"message": "you are not admin"}
    except:
        return "Error occured"


@app.get("/teacher")
async def get_teacher_details(current_user: TokenData = Depends(get_current_user)):   
    try:
        if current_user.role == "teacher":
            return db.teacher_deatils(current_user.username)
        else:
            return {"message": "you are not teacher"}
    except:
        return "Error occured"
       

@app.get("/sublist")
async def get_sublist(current_user: TokenData = Depends(get_current_user)):
    return db.subject_list()

@app.post("/addfaculty")
async def new_faculty(request : TeacherDet, current_user: TokenData = Depends(get_current_user)):
    msg = None
    try:
        if current_user.role == "admin":
            msg = add_new_teacher(request)
        else:
            msg = "you are not admin"
    except:
        msg = "Error occured"
    
    return {"message" : msg}
    

@app.delete('/delstudent')
async def remove_student(request : Studentdel, current_user: TokenData = Depends(get_current_user)):
    try:
        if app.name and app.role == "admin":
            return remove_student(request.sid)
        else:
            return {"message": "you are not admin"}
    except:
        return "Error occured"



if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
