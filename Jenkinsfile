
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'student-management'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        DEPLOYMENT_NAME = 'student-management'
        CONTAINER_NAME = 'student-management'

        // Update this path if your Windows username or kubeconfig location differs.
        KUBECONFIG = 'C:\\Users\\udayk\\.kube\\config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    python --version
                    if ($LASTEXITCODE -ne 0) {
                        throw "Python is not available"
                    }

                    python -m pip install -r requirements.txt
                    if ($LASTEXITCODE -ne 0) {
                        throw "Dependency installation failed"
                    }

                    python -m pip install pytest selenium
                    if ($LASTEXITCODE -ne 0) {
                        throw "Test dependency installation failed"
                    }
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    python -m pytest -v tests/
                    if ($LASTEXITCODE -ne 0) {
                        throw "Tests failed"
                    }
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    docker build -t ${env:IMAGE_NAME}:${env:IMAGE_TAG} .
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker image build failed"
                    }

                    docker tag ${env:IMAGE_NAME}:${env:IMAGE_TAG} ${env:IMAGE_NAME}:latest
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker image tagging failed"
                    }
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    Write-Host "Checking Kubernetes configuration..."

                    if (-not (Test-Path $env:KUBECONFIG)) {
                        throw "Kubeconfig not found at $env:KUBECONFIG. Update the KUBECONFIG environment variable."
                    }

                    kubectl config current-context
                    if ($LASTEXITCODE -ne 0) {
                        throw "No current Kubernetes context is configured for Jenkins"
                    }

                    kubectl get nodes
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes cluster is unavailable to Jenkins"
                    }

                    Write-Host "Applying Kubernetes manifests..."

                    kubectl apply -f deployment.yaml
                    if ($LASTEXITCODE -ne 0) {
                        throw "Failed to apply deployment.yaml"
                    }

                    kubectl apply -f service.yaml
                    if ($LASTEXITCODE -ne 0) {
                        throw "Failed to apply service.yaml"
                    }

                    Write-Host "Updating application image..."

                    kubectl set image deployment/${env:DEPLOYMENT_NAME} ${env:CONTAINER_NAME}=${env:IMAGE_NAME}:${env:IMAGE_TAG}
                    if ($LASTEXITCODE -ne 0) {
                        throw "Failed to update Kubernetes Deployment image"
                    }

                    kubectl rollout status deployment/${env:DEPLOYMENT_NAME} --timeout=120s
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes rollout failed"
                    }

                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }

        always {
            echo 'Jenkins pipeline finished.'
        }
    }
}
