import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- GET /activities ---
def test_get_activities():
    # Arrange
    # (No setup necesario para este test)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_success():
    # Arrange
    email = "test1@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for Chess Club" in response.json()["message"]


def test_signup_duplicate():
    # Arrange
    email = "test2@mergington.edu"
    client.post(f"/activities/Programming Class/signup?email={email}")  # Primer registro

    # Act
    response = client.post(f"/activities/Programming Class/signup?email={email}")  # Duplicado

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# --- DELETE /activities/{activity_name}/signup ---
def test_remove_participant_success():
    # Arrange
    email = "test3@mergington.edu"
    client.post(f"/activities/Gym Class/signup?email={email}")  # Registrar primero

    # Act
    response = client.delete(f"/activities/Gym Class/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from Gym Class" in response.json()["message"]


def test_remove_participant_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Gym Class"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
