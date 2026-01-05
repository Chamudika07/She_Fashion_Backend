from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from . import models
from .database import engine
from .routers import user , schole_shoes , school_shirt


models.Base.metadata.create_all(bind=engine)  #create the database tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(schole_shoes.router)
app.include_router(school_shirt.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

#check git status