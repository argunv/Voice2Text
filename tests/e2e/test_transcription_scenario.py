from fastapi.testclient import TestClient

from app.api.rest.main import app

client = TestClient(app)

def test_transcription_scenario():
    # Health-check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Simulate transcription endpoint
    user_id = 1
    response = client.get(f"/api/transcriptions/{user_id}")
    assert response.status_code == 404  # No transcriptions initially
