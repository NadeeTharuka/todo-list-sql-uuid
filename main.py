from fastapi import FastAPI, Request, Depends, status, Form, Response, Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from db import SessionLocal, engine, DBContext
from sqlalchemy.orm import Session

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    with DBContext() as db:
        yield db

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

@app.get("/tasks")
def get_tasks(request: Request, db: Session = Depends(get_db), user: schemas.User = Depends(manager)):
    return templates.TemplateResponse("tasks.html", {"request": request, 
    "title": "Tasks", 
    "user": user, 
    "tasks": crud.get_tasks_by_user_id(db=db,id=user.id)})

