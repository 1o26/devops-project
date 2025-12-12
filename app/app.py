"""
Flask web application for DevOps CI/CD demonstration.
Provides health check and basic API endpoints.
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Application configuration
APP_VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/", methods=["GET"])
def index():
    """
    Root endpoint that returns application information.
    
    Returns:
        JSON response with app details and timestamp
    """
    logger.info("Index endpoint called")
    return jsonify({
        "message": "Welcome to DevOps CI/CD Application",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "running"
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for Kubernetes probes.
    Used by readiness and liveness probes.
    
    Returns:
        JSON response with health status and HTTP 200
    """
    logger.info("Health check endpoint called")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": APP_VERSION
    }), 200


@app.route("/api/info", methods=["GET"])
def get_info():
    """
    API endpoint that returns detailed application information.
    
    Returns:
        JSON response with app metadata
    """
    logger.info("Info endpoint called")
    return jsonify({
        "application": "DevOps CI/CD Pipeline Demo",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": os.getenv("HOSTNAME", "unknown"),
        "pod_name": os.getenv("POD_NAME", "local"),
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route("/api/metrics", methods=["GET"])
def metrics():
    """
    Metrics endpoint for monitoring.
    Returns application metrics placeholder.
    
    Returns:
        JSON response with basic metrics
    """
    logger.info("Metrics endpoint called")
    return jsonify({
        "uptime_seconds": os.getenv("UPTIME", "unknown"),
        "requests_processed": "N/A",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors gracefully.
    
    Args:
        error: The error object
        
    Returns:
        JSON error response with HTTP 404
    """
    logger.warning(f"404 error: {request.path} not found")
    return jsonify({
        "error": "Endpoint not found",
        "path": request.path,
        "status": 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 internal server errors.
    
    Args:
        error: The error object
        
    Returns:
        JSON error response with HTTP 500
    """
    logger.error(f"500 internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "status": 500
    }), 500


if __name__ == "__main__":
    # Run Flask app
    # In production, this will be run by gunicorn
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
