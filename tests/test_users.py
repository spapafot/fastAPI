from app.config import settings
from app import schemas
from jose import jwt
import pytest


def test_main(client):
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json().get("message") == "THIS IS A NORMAL WEBSITE"


def test_create_user(client):
    response = client.post("/users/", json={"email":"str@gmail.com", "password":"1234"})
    new_user = schemas.UserCreate(**response.json())
    
    assert response.status_code == 201
    assert new_user.email == "str@gmail.com"


def test_user_login(client, test_user):
    response = client.post("/login", data={"username":test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, [settings.algorithm])
    id = payload.get("user_id")
    
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [("str@gmail.com", "password", 403),
                                                          ("email@email.com", None, 422),
                                                          (None, "password", 422),
                                                          (None, None, 422),
                                                          ("str@gmailcom","1234",403)])
def test_incorrect_user_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
        
    assert response.status_code == status_code