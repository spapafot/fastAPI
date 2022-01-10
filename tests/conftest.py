import re
import pytest
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base
from app.oauth2 import create_access_token
from app import models

SQL_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/fastapi_test'
engine = create_engine(SQL_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"str@gmail.com", "password":"123"}
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 201
    
    user = response.json()
    user['password'] = user_data["password"]
    
    return user


@pytest.fixture
def test_another_user(client):
    user_data = {"email":"mik@gmail.com", "password":"123"}
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 201
    
    user = response.json()
    user['password'] = user_data["password"]
    
    return user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_another_user, session):
    posts = [{"title": "Title 1", "content": "Content of post 1", "user_id": test_user["id"]},
             {"title": "Title 2", "content": "Content of post 2", "user_id": test_user["id"]},
             {"title": "Title 3", "content": "Content of post 3", "user_id": test_user["id"]},
             {"title": "Title 4", "content": "Content of post 4", "user_id": test_another_user["id"]},
             {"title": "Title 5", "content": "Content of post 5", "user_id": test_another_user["id"]}]

    session.add_all(models.Post(**post) for post in posts)
    session.commit()
    return session.query(models.Post).all()