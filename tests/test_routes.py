from src.models.models import User, Group, Post

from http.cookies import SimpleCookie



# UTILS

# request to /auth/login is enough to receive a token as an httpOnly cookie
# no need to parse the cookie
def get_access_token(client, username, password):
  response = client.post("/auth/login", data={
      "username": username,
      "password": password,
    }, follow_redirects=True
  )
  # set_cookie_header = response.headers.get("Set-Cookie")
  # cookies = SimpleCookie()
  # cookies.load(set_cookie_header)
  # data = cookies.get("access_token")
  # return data


def remove_access_token(client):
  response = client.post("/auth/logout", follow_redirects=True)


# the same error as in create_user fixture (werkzeug Response object)
#TypeError: Response.__call__() missing 1 required positional argument: 'start_response'
def create_user(client, username, email, password):
  response = client.post(
    "/auth/register",
    data={"username": username, "email": email, "password": password},
    follow_redirects=True
  )
  return response


# TESTS

def test_create_user(client):
  response = client.post(
    "/auth/register",
    data={"username": "testuser1", "email": "test1@email.com", "password": "testpassword1"},
    follow_redirects=True
  )
  
  user = User.query.filter_by(name="testuser1").first()
  assert user is not None
  assert response.status_code == 200


def test_create_post(client, create_user):
  # create user fixture
  # create_user(client)
  
  # create user
  client.post(
    "/auth/register",
    data={"username": "testuser1", "email": "test1@email.com", "password": "testpassword1"},
    follow_redirects=True
  )
  # the token is auto-added to the header in consequent requests by the client 
  token = get_access_token(client, "testuser1", "testpassword1")

  # create post
  response = client.post("/create", data={
      "title": "test post1",
      "body": "test text 1"
    },
    # headers={"Authorization": f"Bearer {token}"}
  )
  
  posts = Post.query.filter_by(title="test post1").first()
  assert posts is not None
  assert response.status_code == 302


def test_update_post(client):
  # create user
  client.post(
    "/auth/register",
    data={"username": "testuser1", "email": "test1@email.com", "password": "testpassword1"},
    follow_redirects=True
  )
  
  get_access_token(client, "testuser1", "testpassword1")

  # create post
  client.post("/create", data={
      "title": "test post1",
      "body": "test text 1"
    }
  )
  
  # update post
  response = client.post("/1/update", data={
      "title": "test post1 updated",
      "body": "test text 1 updated"
    }
  )
  
  posts = Post.query.filter_by(title="test post1 updated").first()
  assert posts is not None
  assert response.status_code == 302


def test_delete_post(client):
  # create user
  client.post(
    "/auth/register",
    data={"username": "testuser1", "email": "test1@email.com", "password": "testpassword1"},
    follow_redirects=True
  )

  get_access_token(client, "testuser1", "testpassword1")

  # create post
  client.post("/create", data={
      "title": "test post1",
      "body": "test text 1"
    }
  )
  
  # delete post
  response = client.post("/1/delete")
  
  posts = Post.query.all()
  assert posts == []
  assert response.status_code == 302
