import pytest
from app.schemes import UserOut
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email":"hello1237@gmail.com",
                  "password":"password123"}
    response = client.post("/users/", json=user_data)

    new_user = response.json()
    new_user["password"] = user_data["password"]
    assert response.status_code == 201
    return new_user


def test_create_user(client):
    response = client.post("/users/", json={"email":"hello1237@gmail.com", "password":"password123"})
    new_user = UserOut(**response.json())
    assert new_user.email == "hello1237@gmail.com"
    assert response.status_code == 201    

def test_login_user(client, test_user):
    response = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})
    assert response.status_code == 200