def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id":test_posts[0].id, "dir":1})
    assert response.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts):
    vote_data = {"post_id":test_posts[0].id, "dir":1}

    response1 = authorized_client.post("/vote/", json=vote_data)
    assert response1.status_code == 201

    response2 = authorized_client.post("/vote/", json=vote_data)
    assert response2.status_code == 409
    
def test_delete_vote(authorized_client, test_posts):
    vote_data_add = {"post_id": test_posts[1].id, "dir": 1}
    response_add = authorized_client.post("/vote/", json=vote_data_add)
    assert response_add.status_code == 201

    vote_data_delete = {"post_id": test_posts[1].id, "dir": 0}
    response_delete = authorized_client.post("/vote/", json=vote_data_delete)
    assert response_delete.status_code == 201 

def test_delete_vote_non_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id":test_posts[0].id, "dir":0})
    assert response.status_code == 404

def test_vote_post_non_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id":999999, "dir":1})
    assert response.status_code == 404

def test_vote_unauthorized(client, test_posts):
    response = client.post("/vote/", json={"post_id":test_posts[0].id, "dir":1})
    assert response.status_code == 401

def test_delete_vote_unauthorized(client, test_posts):
    response = client.post("/vote/", json={"post_id":test_posts[0].id, "dir":0})
    assert response.status_code == 401















