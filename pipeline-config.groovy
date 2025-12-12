"""
Jenkins Pipeline Configuration Variables
Central location for pipeline parameters
"""

// Docker Registry Configuration
def DOCKER_REGISTRY = [
    url: 'docker.io',
    image_name: 'mydockerhubuser/my-devops-app'
]

// Kubernetes Configuration
def KUBERNETES = [
    namespace: 'default',
    deployment_name: 'devops-app',
    replicas: 2
]

// Application Configuration
def APP_CONFIG = [
    port: 5000,
    environment: 'production',
    version: '1.0.0'
]

// Slack Configuration
def SLACK = [
    channel: '#devops',
    username: 'Jenkins Bot',
    icon_emoji: ':jenkins:'
]

// Build Configuration
def BUILD_CONFIG = [
    timeout_minutes: 30,
    concurrent_builds: false,
    build_history: 30
]
