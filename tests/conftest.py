from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Post
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
        yield session
    app.dependency_overrides[get_db] = override_get_db   
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email":"hello1237@gmail.com",
                  "password":"password123"}
    response = client.post("/users/", json=user_data)

    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"hello1238@gmail.com",
                  "password":"password123"}
    response = client.post("/users/", json=user_data)

    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user    

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title":"first title user1", "content":"first content user1", "owner_id":test_user["id"]},
        {"title":"second title user1", "content":"second content user1", "owner_id":test_user["id"]},
        {"title":"first title user2", "content":"first content user2", "owner_id":test_user2["id"]},
        {"title":"second title user2", "content":"second content user2", "owner_id":test_user2["id"]}
    ]
    posts = [Post(**data) for data in posts_data]

    session.add_all(posts)
    session.commit()
    all_posts = session.query(Post).all()
    return all_posts

@pytest.fixture
def test_vote(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = authorized_client.post("/vote/", json=vote_data)
    return response.json()

@pytest.fixture
def test_delete_vote(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[1].id, "dir": 0}
    response = authorized_client.post("/vote/", json=vote_data)
    return response.json()
