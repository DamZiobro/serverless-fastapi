"""Unit tests of FasAPI-based API"""
from fastapi.testclient import TestClient

from api import __version__
from api.main import app

client = TestClient(app)


def test_version():
    """Testing API version."""
    assert __version__ == "1.0.1"


def test_get_hello_returns_200():
    """GET /hello returns 200."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_root_hello_returns_200():
    """GET / returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API version: 1.0.1"}
