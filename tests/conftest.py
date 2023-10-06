import pytest
from src import create_app
from src.db import db

@pytest.fixture
def client(scope="session"):
  app = create_app()
  with app.test_client() as client:
    with app.app_context():
      db.create_all()
      db.session.commit()
        
      yield client
  
  with app.app_context():
    db.drop_all()
    db.session.commit()

# errors out
#TypeError: Response.__call__() missing 1 required positional argument: 'start_response'
@pytest.fixture
def create_user(client):
  response = client.post(
    "/auth/register",
    data={"username": "testuser1", "email": "test1@email.com", "password": "testpassword1"},
    follow_redirects=True
  )
  return response
