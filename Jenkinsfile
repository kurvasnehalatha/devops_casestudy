
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'student-management'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        DEPLOYMENT_NAME = 'student-management'
        CONTAINER_NAME = 'student-management'
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
                    python --version
                    python -m pip install -r requirements.txt
                    python -m pip install pytest selenium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    python -m pytest -v tests/
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                powershell '''
                    docker build -t ${env:IMAGE_NAME}:${env:IMAGE_TAG} .
                    if ($LASTEXITCODE -ne 0) {
                        exit $LASTEXITCODE
                    }

                    docker tag ${env:IMAGE_NAME}:${env:IMAGE_TAG} ${env:IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                powershell '''
                    kubectl config current-context
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes context is not available"
                    }

                    kubectl set image deployment/${env:DEPLOYMENT_NAME} ${env:CONTAINER_NAME}=${env:IMAGE_NAME}:${env:IMAGE_TAG}
                    if ($LASTEXITCODE -ne 0) {
                        throw "Failed to update Kubernetes Deployment"
                    }

                    kubectl rollout status deployment/${env:DEPLOYMENT_NAME} --timeout=120s
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes rollout failed"
                    }
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
