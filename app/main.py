from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.param_functions import Body
from passlib.utils.decor import deprecated_function
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .routers import user,post, auth


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="StrAfm0569", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f"Connection Failed Error:\n{error}")
        time.sleep(15)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "THIS IS A NORMAL WEBSITE"}




