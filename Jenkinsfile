#!/usr/bin/env groovy

/**
 * DevOps CI/CD Pipeline
 * 
 * This declarative Jenkins pipeline automates the complete software delivery process:
 * - Builds Docker images
 * - Runs unit tests
 * - Performs code quality checks
 * - Pushes images to Docker Hub
 * - Deploys to Kubernetes
 * - Sends Slack notifications
 * 
 * Prerequisites:
 * - Jenkins with Docker and kubectl installed
 * - Docker Hub credentials (ID: DOCKERHUB_CREDS)
 * - Kubernetes credentials (ID: KUBE_CONFIG)
 * - Slack webhook configured
 */

pipeline {
    agent any
    
    // Pipeline parameters
    parameters {
        string(name: 'DOCKER_REGISTRY_URL', defaultValue: 'docker.io', description: 'Docker Registry URL')
        string(name: 'KUBE_NAMESPACE', defaultValue: 'default', description: 'Kubernetes Namespace')
    }
    
    // Environment variables
    environment {
        // Docker configuration
        IMAGE = "tusharmv266/my-devops-app"
        TAG = "${BUILD_NUMBER}"
        REGISTRY_URL = "${params.DOCKER_REGISTRY_URL}"
        DOCKER_CREDENTIALS = credentials('DOCKERHUB_CREDS')
        
        // Kubernetes configuration
        KUBE_NAMESPACE = "${params.KUBE_NAMESPACE}"
        
        // Application settings
        ENVIRONMENT = "production"
        APP_PORT = "5000"
        
        // Build settings
        BUILD_TIMESTAMP = "${BUILD_TIMESTAMP}"
        GIT_COMMIT_SHORT = "${GIT_COMMIT.take(7)}"
    }
    
    options {
        // Limit concurrent builds
        disableConcurrentBuilds()
        
        // Keep build logs for last 30 builds
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        
        // Timeout pipeline after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        
        // Add timestamps to console output
        timestamps()
    }
    
    stages {
        /**
         * CHECKOUT STAGE
         * Clones the repository and prepares workspace
         */
        stage('Checkout') {
            steps {
                script {
                    echo "========== Checkout Stage =========="
                    echo "Cloning repository from ${GIT_URL}"
                    echo "Branch: ${GIT_BRANCH}"
                    echo "Commit: ${GIT_COMMIT_SHORT}"
                }
                
                // Clean workspace before checkout
                cleanWs()
                
                // Checkout the repository
                checkout scm
                
                script {
                    echo "Workspace prepared and repository cloned successfully"
                }
            }
        }
        
        /**
         * LINT STAGE
         * Performs code quality checks using flake8
         * Checks for PEP8 compliance and code style issues
         */
        stage('Lint') {
            steps {
                script {
                    echo "========== Lint Stage =========="
                    echo "Running flake8 code quality checks..."
                }
                
                // Run flake8 linter on Python code
                bat '''
                    @echo off
                    echo Installing flake8...
                    pip install flake8 -q
                    
                    echo Running flake8 on app/app.py...
                    flake8 app/app.py --count --select=E9,F63,F7,F82 --show-source --statistics
                    
                    echo Full flake8 report:
                    flake8 app/app.py --statistics
                '''
                
                script {
                    echo "Code quality checks completed"
                }
            }
        }
        
        /**
         * UNIT TESTS STAGE
         * Runs pytest test suite with coverage reporting
         * Validates application functionality before deployment
         */
        stage('Unit Tests') {
            steps {
                script {
                    echo "========== Unit Tests Stage =========="
                    echo "Running pytest unit tests..."
                }
                
                // Run tests with coverage
                bat '''
                    @echo off
                    echo Installing test dependencies...
                    pip install -r app/requirements.txt -q
                    
                    echo Running pytest tests...
                    pytest tests/test_app.py -v --tb=short --junit-xml=test-results.xml --cov=app --cov-report=html --cov-report=term
                '''
                
                script {
                    echo "Unit tests completed successfully"
                }
                
                // Publish test results
                junit 'test-results.xml'
                publishHTML([
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
        
        /**
         * DOCKER BUILD STAGE
         * Builds Docker image with multi-stage optimization
         * Tags with build number and commit SHA
         */
        stage('Docker Build') {
            steps {
                script {
                    echo "========== Docker Build Stage =========="
                    echo "Building Docker image: ${IMAGE}:${TAG}"
                }
                
                // Build Docker image
                bat '''
                    @echo off
                    echo Building Docker image with tag %TAG%...
                    docker build -t %IMAGE%:%TAG% -t %IMAGE%:latest --label "BUILD_NUMBER=%BUILD_NUMBER%" --label "GIT_COMMIT=%GIT_COMMIT_SHORT%" --label "BUILD_TIMESTAMP=%BUILD_TIMESTAMP%" -f docker/Dockerfile .
                    
                    echo Docker image built successfully
                    docker images | findstr "%IMAGE%"
                '''
                
                script {
                    echo "Image build completed"
                }
            }
        }
        
        /**
         * DOCKER PUSH STAGE
         * Authenticates with Docker Hub and pushes image
         * Uses DOCKERHUB_CREDS credentials for authentication
         */
        stage('Docker Push') {
            steps {
                script {
                    echo "========== Docker Push Stage =========="
                    echo "Pushing Docker image to registry: ${REGISTRY_URL}"
                }
                
                // Login to Docker Hub and push image
                bat '''
                    @echo off
                    echo Authenticating with Docker Hub...
                    docker login -u %DOCKER_CREDENTIALS_USR% -p %DOCKER_CREDENTIALS_PSW%
                    
                    echo Pushing image: %IMAGE%:%TAG%
                    docker push %IMAGE%:%TAG%
                    
                    echo Pushing latest tag...
                    docker push %IMAGE%:latest
                    
                    echo Image pushed successfully
                    docker logout
                '''
                
                script {
                    echo "Docker image pushed to registry"
                }
            }
        }
        
        /**
         * KUBERNETES DEPLOY STAGE
         * Deploys application to Kubernetes cluster
         * Uses kubectl to apply manifests and update deployment
         * Will skip if KUBE_CONFIG credential is not configured
         */
        stage('Kubernetes Deploy') {
            steps {
                script {
                    echo "========== Kubernetes Deploy Stage =========="
                    echo "Deploying to Kubernetes namespace: ${KUBE_NAMESPACE}"
                    
                    // Check if KUBE_CONFIG credential exists
                    def kubeConfigExists = false
                    try {
                        withCredentials([file(credentialsId: 'KUBE_CONFIG', variable: 'KUBECONFIG_FILE')]) {
                            kubeConfigExists = true
                            echo "KUBE_CONFIG credential found - proceeding with deployment"
                            
                            sh '''
                                echo "Setting up kubeconfig..."
                                export KUBECONFIG=${KUBECONFIG_FILE}
                                
                                echo "Verifying kubectl connectivity..."
                                kubectl cluster-info
                                kubectl get nodes
                                
                                echo "Applying Kubernetes manifests..."
                                kubectl apply -f k8s/service.yaml -n ${KUBE_NAMESPACE}
                                kubectl apply -f k8s/deployment.yaml -n ${KUBE_NAMESPACE}
                                
                                echo "Updating deployment image to ${IMAGE}:${TAG}..."
                                kubectl set image deployment/devops-app \
                                    devops-app=${IMAGE}:${TAG} \
                                    -n ${KUBE_NAMESPACE}
                                
                                echo "Applying optional ingress configuration..."
                                kubectl apply -f k8s/ingress.yaml -n ${KUBE_NAMESPACE} || true
                                
                                echo "Waiting for deployment rollout..."
                                kubectl rollout status deployment/devops-app -n ${KUBE_NAMESPACE} --timeout=5m
                                
                                echo "Deployment completed successfully"
                                echo "Getting pod information..."
                                kubectl get pods -n ${KUBE_NAMESPACE} -l app=devops-app
                            '''
                        }
                    } catch (Exception e) {
                        echo "⚠️  KUBE_CONFIG credential not found - skipping Kubernetes deployment"
                        echo "To enable K8s deployment, create a 'KUBE_CONFIG' secret file credential in Jenkins"
                        echo "Continuing with pipeline..."
                    }
                }
            }
        }
    }
    
    /**
     * POST ACTIONS
     * Executed after all stages complete
     */
    post {
        success {
            echo "========== BUILD SUCCESS =========="
            echo "Build #${BUILD_NUMBER} completed successfully"
            echo "Docker Image: ${IMAGE}:${TAG}"
        }
        
        failure {
            echo "========== BUILD FAILED =========="
            echo "Build #${BUILD_NUMBER} failed - check logs above for details"
        }
        
        unstable {
            echo "========== BUILD UNSTABLE =========="
            echo "Build #${BUILD_NUMBER} completed with warnings"
        }
    }
}
