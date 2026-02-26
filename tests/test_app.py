import copy

import pytest
from fastapi.testclient import TestClient

from src import app


# create a client once for all tests
client = TestClient(app.app)

# snapshot of the initial activities so we can restore it
INITIAL_ACTIVITIES = copy.deepcopy(app.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the global `activities` dictionary before each test.
    The fixture is applied automatically to every test (autouse).
    """
    app.activities = copy.deepcopy(INITIAL_ACTIVITIES)
    yield
    app.activities = copy.deepcopy(INITIAL_ACTIVITIES)


def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app.activities[activity]["participants"]


def test_unregister_from_activity_success():
    # Arrange: sign the student up first so they can be removed
    activity = "Chess Club"
    email = "tempstudent@mergington.edu"
    client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in app.activities[activity]["participants"]
