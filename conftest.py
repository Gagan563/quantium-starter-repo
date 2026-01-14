import pytest
from app import app


@pytest.fixture
def dash_app():
    """Fixture to provide the Dash app for testing"""
    return app
