from fastapi import FastAPI, Request, APIRouter,Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from fastapi.responses import HTMLResponse


app = FastAPI()
app.name = "ravi"
app.secret = "ghjklsdfghjklsxdcfvgbhnjmkxcvbnmkdfghj"


oth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.get("/")
async def now():
    return app.name, app.secret

@app.post("/home")
async def the(request_form : OAuth2PasswordRequestForm = Depends(oth2_scheme)):
    return request_form



if __name__ == "__main__":
    uvicorn.run("trial:app", host='localhost', port=8000, reload=True)
    print(app.name)
    print(app.secret)
    print("fghjk")