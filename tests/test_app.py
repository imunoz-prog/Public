import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- GET /activities ---
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=test1@mergington.edu")
    assert response.status_code == 200
    assert "Signed up test1@mergington.edu for Chess Club" in response.json()["message"]


def test_signup_duplicate():
    email = "test2@mergington.edu"
    # First signup
    client.post(f"/activities/Programming Class/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# --- DELETE /activities/{activity_name}/signup ---
def test_remove_participant_success():
    email = "test3@mergington.edu"
    # Register first
    client.post(f"/activities/Gym Class/signup?email={email}")
    # Remove
    response = client.delete(f"/activities/Gym Class/signup?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from Gym Class" in response.json()["message"]


def test_remove_participant_not_found():
    response = client.delete("/activities/Gym Class/signup?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_activity_not_found():
    response = client.delete("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
