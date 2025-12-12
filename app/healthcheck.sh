#!/bin/bash
#
# Health check script for the Flask application
# Used by Docker and Kubernetes health checks
# Checks if the /health endpoint returns a 200 status code
#

HEALTH_ENDPOINT="${HEALTH_ENDPOINT:-http://localhost:5000/health}"
TIMEOUT="${TIMEOUT:-5}"

# Perform the health check request
response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout "$TIMEOUT" "$HEALTH_ENDPOINT")

# Check if response is 200
if [ "$response" -eq 200 ]; then
    echo "Application is healthy (HTTP $response)"
    exit 0
else
    echo "Application health check failed (HTTP $response)"
    exit 1
fi
