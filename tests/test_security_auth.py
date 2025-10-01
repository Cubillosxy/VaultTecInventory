# tests/test_security_auth.py
import importlib
import pytest
import jwt
from fastapi.testclient import TestClient

import inventory.interfaces.http.security as security_mod
import inventory.interfaces.http.api as api_mod


@pytest.fixture(autouse=True)
def jwt_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("JWT_ALG", "HS256")
    monkeypatch.setenv("JWT_EXPIRES_MIN", "5")
    # Auth dev user for /auth/token
    monkeypatch.setenv("DEV_USER", "test")
    monkeypatch.setenv("DEV_PASS", "test")
    # Reload modules so they pick up new env
    importlib.reload(security_mod)
    importlib.reload(api_mod)


@pytest.fixture()
def client():
    # Use the reloaded app
    return TestClient(api_mod.app)


def test_create_and_decode_token():
    token = security_mod.create_access_token("test", {"role": "admin"})
    payload = jwt.decode(token, "test-secret", algorithms=["HS256"])
    assert payload["sub"] == "test"
    assert payload["role"] == "admin"   # <-- was 'test' before; should be 'admin'
    assert "exp" in payload and "iat" in payload


def test_require_user_valid_token():
    token = security_mod.create_access_token("user1")
    payload = security_mod.require_user(token=token)  # call directly; no __wrapped__ needed
    assert payload["sub"] == "user1"


def test_require_user_invalid_token():
    with pytest.raises(Exception):
        security_mod.require_user(token="not-a-token")


def test_auth_issue_token_endpoint(client: TestClient):
    r = client.post(
        "/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "test", "password": "test"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str) and body["access_token"]
