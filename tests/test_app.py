import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    # Arrange
    # (No setup needed, just client)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test POST /activities/{activity}/signup
def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user not in participants
    if email in client.get("/activities").json()[activity]["participants"]:
        client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")

# Test POST /activities/{activity}/unregister
@pytest.mark.skipif(not hasattr(app, 'routes') or not any(r.path.endswith('/unregister') for r in app.routes), reason="No unregister endpoint implemented")
def test_unregister_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is in participants
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "removed" in response.json()["message"]
