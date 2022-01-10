import json
import pytest
from app import schemas

def test_get_all_posts(client, test_posts):
    response = client.get("/posts/")  
    
    def validate(post):
        return schemas.PostOut(**post)
    posts = list(map(validate, response.json()))

    assert response.status_code == 200


def test_get_all_posts_authorized(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/")
    assert response.status_code == 200


def test_get_one_post_authorized(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200


def test_get_one_post_unauthorized(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200


def test_post_does_not_exist(client, test_posts):
    response = client.get(f"/posts/100000000000000000")
    assert response.status_code == 404


def test_post_invalid_url(client, test_posts):
    response = client.get(f"/posts/string")
    assert response.status_code == 422


def test_delete_post_unauthorized(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_authorized(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert response.status_code == 401


@pytest.mark.parametrize("title, content, published",[("Title 1", "Content 1", True), ("Title 2", "Content 2", False)])
def test_create_post(authorized_client, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.PostCreate(**response.json())
    assert response.status_code == 201


def test_create_post_unauthorized(client):
    response = client.post("/posts/", json={"title": "Any title", "content": "Any content"})
    assert response.status_code == 401

####
def test_update_post_unauthorized(client, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}", json={"title": "Any title", "content": "Any content"})
    assert response.status_code == 401


def test_update_post_authorized(authorized_client, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title": "New Title", "content": "Updated Content"})
    updated_post = schemas.Post(**response.json())
    assert updated_post.content == "Updated Content"
    assert response.status_code == 200


def test_update_other_user_post(authorized_client, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[4].id}", json={"title":"NOT AUTHORIZED", "content":"NOT AUTHORIZED"})
    assert response.status_code == 403