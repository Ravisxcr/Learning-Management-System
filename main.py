from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import database as db
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="/templates")



@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.get("/student")
async def getstudentdetails():
    return db.student_deatils()

@app.get("/teacher")
async def getteacherdetails():
    return db.teacher_deatils()


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
