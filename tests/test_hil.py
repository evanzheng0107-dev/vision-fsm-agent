"""Tests for the HIL server and client."""
import pytest

from hil_server import app


@pytest.fixture
def client():
    """Flask test client with a clean store."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        # Reset stores before each test.
        c.post("/hil/reset")
        yield c
        c.post("/hil/reset")


def test_status(client):
    resp = client.get("/hil/status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "running"
    assert data["correction_count"] == 0


def test_set_and_get_correction(client):
    correction = {
        "type": "correct",
        "action": "click",
        "correct_params": {"x": 10, "y": 20},
        "reason": "test",
    }
    resp = client.post("/hil/set_correction", json=correction)
    assert resp.status_code == 200

    resp = client.get("/hil/get_correction")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["type"] == "correct"
    assert data["action"] == "click"

    # Second get should return "none" (one-shot).
    resp = client.get("/hil/get_correction")
    assert resp.get_json()["type"] == "none"


def test_get_correction_empty(client):
    resp = client.get("/hil/get_correction")
    assert resp.status_code == 200
    assert resp.get_json()["type"] == "none"


def test_set_correction_missing_fields(client):
    resp = client.post("/hil/set_correction", json={"type": "correct"})
    assert resp.status_code == 400


def test_send_correction_learning(client):
    payload = {
        "type": "manual_correction",
        "script_id": "test",
        "correction": {"action": "click"},
    }
    resp = client.post("/hil/send_correction", json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "success"

    resp = client.get("/hil/status")
    assert resp.get_json()["learning_count"] == 1


def test_send_status(client):
    resp = client.post("/hil/send_status", json={"type": "agent_status", "status": {}})
    assert resp.status_code == 200
    assert client.get("/hil/status").get_json()["status_count"] == 1


def test_get_decision_stub(client):
    resp = client.post("/hil/get_decision", json={"type": "request_decision"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "action" in data


def test_reset(client):
    client.post("/hil/set_correction", json={
        "type": "correct", "action": "click", "correct_params": {"x": 1, "y": 2}
    })
    resp = client.post("/hil/reset")
    assert resp.status_code == 200
    assert client.get("/hil/status").get_json()["correction_count"] == 0


def test_hil_client_validation():
    """The HilClient validation logic should reject malformed corrections."""
    from hil_client import HilClient

    assert HilClient._validate_correction({"type": "none"}) is True
    assert HilClient._validate_correction({
        "type": "correct", "action": "click", "correct_params": {"x": 1, "y": 2}
    }) is True
    assert HilClient._validate_correction({"type": "correct"}) is False
    assert HilClient._validate_correction({
        "type": "correct", "action": "click", "correct_params": {}
    }) is False
