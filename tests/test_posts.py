from app.schemes import PostWithVotes, Post, UserOut
import pytest

# Helper function to find a post owned by a specific user ID
def find_post_by_owner(posts, owner_id):
    for post in posts:
        if post.owner_id == owner_id:
            return post
    return None

# --- Test Getting Posts ---

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == len(test_posts) 

    posts_from_api = [PostWithVotes(**p) for p in response_data]

    original_post_ids = {p.id for p in test_posts}
    response_post_ids = {p.id for p in posts_from_api}
    assert original_post_ids == response_post_ids

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_get_one_post(authorized_client, test_user, test_posts):
    user_post = find_post_by_owner(test_posts, test_user['id'])
    assert user_post is not None 

    response = authorized_client.get(f"/posts/{user_post.id}")
    assert response.status_code == 200
    post = PostWithVotes(**response.json())
    assert post.id == user_post.id
    assert post.title == user_post.title
    assert post.content == user_post.content
    assert post.owner_id == test_user['id']
    assert post.owner.id == test_user['id'] 

def test_get_one_post_not_exist(authorized_client): 
    response = authorized_client.get("/posts/999999") 
    assert response.status_code == 404

def test_unauthorized_user_get_one_post(client, test_user, test_posts):
    user_post = find_post_by_owner(test_posts, test_user['id'])
    assert user_post is not None
    response = client.get(f"/posts/{user_post.id}")
    assert response.status_code == 401

# --- Test Creating Posts ---

@pytest.mark.parametrize("title, content, published", [
    ("Param test title 1", "Param test content 1", True),
    ("Param test title 2", "Param test content 2", False),
    ("Param test title 3", "Param test content 3", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )
    assert response.status_code == 201
    created_post = Post(**response.json()) 
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    
    if hasattr(created_post, 'owner') and isinstance(created_post.owner, UserOut):
         assert created_post.owner.id == test_user['id']
         assert created_post.owner.email == test_user['email']

def test_create_post_default_published_true(authorized_client, test_user): 
    response = authorized_client.post(
        "/posts/",
        json={"title": "Default pub title", "content": "Default pub content"} 
    )
    assert response.status_code == 201
    created_post = Post(**response.json())
    assert created_post.published == True 
    assert created_post.title == "Default pub title"
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client): 
    response = client.post(
        "/posts/",
        json={"title": "unauthorized title", "content": "unauthorized content"} 
    )
    assert response.status_code == 401

# --- Test Updating Posts ---

def test_update_post(authorized_client, test_user, test_posts):
    user_post = find_post_by_owner(test_posts, test_user['id'])
    assert user_post is not None

    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False 
    }
    response = authorized_client.put(f"/posts/{user_post.id}", json=data)
    assert response.status_code == 200
    updated_post = Post(**response.json())
    assert updated_post.id == user_post.id
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.published == data["published"]
    assert updated_post.owner_id == test_user['id']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
   
    other_user_post = find_post_by_owner(test_posts, test_user2['id'])
    assert other_user_post is not None 

    data = {"title": "updated by wrong user", "content": "updated by wrong user"}
    
    response = authorized_client.put(f"/posts/{other_user_post.id}", json=data)
    assert response.status_code == 403 

def test_unauthorized_user_update_post(client, test_user, test_posts):
    user_post = find_post_by_owner(test_posts, test_user['id'])
    assert user_post is not None
    data = {"title": "update unauthorized", "content": "update unauthorized"}
    response = client.put(f"/posts/{user_post.id}", json=data)
    assert response.status_code == 401

def test_update_post_does_not_exist(authorized_client, test_user):
    data = {"title": "update non-exist", "content": "update non-exist"}
    response = authorized_client.put("/posts/999999", json=data)
    assert response.status_code == 404

# --- Test Deleting Posts ---

def test_delete_post(authorized_client, test_user, test_posts):
    user_post_from_fixture = find_post_by_owner(test_posts, test_user['id'])
    assert user_post_from_fixture is not None

    post_id_to_delete = user_post_from_fixture.id
  
    response = authorized_client.delete(f"/posts/{post_id_to_delete}")
    assert response.status_code == 204

    response_get = authorized_client.get(f"/posts/{post_id_to_delete}")
    assert response_get.status_code == 404

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    user_post = find_post_by_owner(test_posts, test_user['id'])
    assert user_post is not None
    response = client.delete(f"/posts/{user_post.id}")
    assert response.status_code == 401

def test_delete_post_does_not_exist(authorized_client, test_user): 
    response = authorized_client.delete("/posts/999999")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_user2, test_posts):
    other_user_post = find_post_by_owner(test_posts, test_user2['id'])
    assert other_user_post is not None 

    response = authorized_client.delete(f"/posts/{other_user_post.id}")
    assert response.status_code == 403 

























