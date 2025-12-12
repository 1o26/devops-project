"""
Unit tests for the Flask application.
Tests all endpoints and error handling.
Run with: pytest tests/test_app.py -v --cov=app
"""

import pytest
import json
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.app import app


@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask app.
    Uses testing mode for better error reporting.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestIndexEndpoint:
    """Test cases for the root endpoint."""
    
    def test_index_returns_200(self, client):
        """Test that index endpoint returns HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_index_returns_json(self, client):
        """Test that index endpoint returns valid JSON."""
        response = client.get("/")
        assert response.content_type == "application/json"
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_index_contains_required_fields(self, client):
        """Test that index response contains required fields."""
        response = client.get("/")
        data = json.loads(response.data)
        assert "message" in data
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data
        assert "status" in data
    
    def test_index_message_content(self, client):
        """Test that index message is correct."""
        response = client.get("/")
        data = json.loads(response.data)
        assert data["message"] == "Welcome to DevOps CI/CD Application"
        assert data["status"] == "running"


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_returns_200(self, client):
        """Test that health endpoint returns HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_json(self, client):
        """Test that health endpoint returns valid JSON."""
        response = client.get("/health")
        assert response.content_type == "application/json"
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_health_status_is_healthy(self, client):
        """Test that health endpoint status is 'healthy'."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"
    
    def test_health_contains_required_fields(self, client):
        """Test that health response contains required fields."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
    
    def test_health_multiple_requests(self, client):
        """Test that health endpoint handles multiple requests."""
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200


class TestInfoEndpoint:
    """Test cases for the info endpoint."""
    
    def test_info_returns_200(self, client):
        """Test that info endpoint returns HTTP 200."""
        response = client.get("/api/info")
        assert response.status_code == 200
    
    def test_info_returns_json(self, client):
        """Test that info endpoint returns valid JSON."""
        response = client.get("/api/info")
        assert response.content_type == "application/json"
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_info_contains_required_fields(self, client):
        """Test that info response contains required fields."""
        response = client.get("/api/info")
        data = json.loads(response.data)
        assert "application" in data
        assert "version" in data
        assert "environment" in data


class TestMetricsEndpoint:
    """Test cases for the metrics endpoint."""
    
    def test_metrics_returns_200(self, client):
        """Test that metrics endpoint returns HTTP 200."""
        response = client.get("/api/metrics")
        assert response.status_code == 200
    
    def test_metrics_returns_json(self, client):
        """Test that metrics endpoint returns valid JSON."""
        response = client.get("/api/metrics")
        assert response.content_type == "application/json"
        data = json.loads(response.data)
        assert isinstance(data, dict)


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_404_error_handling(self, client):
        """Test that 404 errors are handled properly."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
        assert data["error"] == "Endpoint not found"
    
    def test_404_contains_path(self, client):
        """Test that 404 response contains the requested path."""
        response = client.get("/invalid/endpoint")
        data = json.loads(response.data)
        assert "path" in data
        assert "/invalid/endpoint" in data["path"]
    
    def test_method_not_allowed(self, client):
        """Test that unsupported HTTP methods are rejected."""
        response = client.post("/")
        assert response.status_code == 405  # Method Not Allowed


class TestContentTypes:
    """Test cases for correct content types."""
    
    def test_all_endpoints_return_json(self, client):
        """Test that all endpoints return JSON content type."""
        endpoints = ["/", "/health", "/api/info", "/api/metrics"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.content_type == "application/json"


class TestResponseValidation:
    """Test cases for response validation."""
    
    def test_timestamp_format(self, client):
        """Test that all responses contain ISO format timestamps."""
        response = client.get("/health")
        data = json.loads(response.data)
        timestamp = data["timestamp"]
        # ISO format timestamp should contain 'T'
        assert "T" in timestamp
    
    def test_version_format(self, client):
        """Test that version is in semantic versioning format."""
        response = client.get("/health")
        data = json.loads(response.data)
        version = data["version"]
        # Version should contain dots (e.g., "1.0.0")
        assert "." in version


class TestApplicationHealth:
    """Integration tests for application health."""
    
    def test_app_startup(self, client):
        """Test that app starts without errors."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_rapid_health_checks(self, client):
        """Test app stability under rapid health checks."""
        for _ in range(10):
            response = client.get("/health")
            assert response.status_code == 200
    
    def test_mixed_endpoint_calls(self, client):
        """Test app stability with mixed endpoint calls."""
        endpoints = ["/", "/health", "/api/info", "/api/metrics"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, dict)


if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([__file__, "-v", "--cov=app"])
