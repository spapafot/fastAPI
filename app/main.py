from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="StrAfm0569", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f"Connection Failed Error:\n{error}")
        time.sleep(15)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {
    "title": "Title 1",
    "content": "This is the content",
    "id": 1
    },
    {
    "title": "Title 1",
    "content": "This is the content",
    "id": 2
    }
]

def find_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i


def find_post_index(id: int):
    for idx, i in enumerate(my_posts):
        if i['id'] == id:
            return idx


@app.get("/")
async def root():
    return {"message": "Hello World..."}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VAlUES (%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Does Not Exist") 
    return {"data":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Does Not Exist")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Does Not Exist") 
    conn.commit()
    return {"data": post}

    
