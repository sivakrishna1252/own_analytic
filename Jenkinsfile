pipeline {
    agent any

    environment {
        // Application configuration
        APP_NAME = 'analytics-backend'
        DOCKER_IMAGE = "analyatics-web"
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull code from the repository
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                echo 'Building Docker Image...'
                // Build the image using the local Dockerfile
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Deploy Local') {
            steps {
                echo 'Deploying application with Docker Compose...'
                // Restarts the containers and applies migrations
                sh """
                    docker-compose down
                    docker-compose up -d --build
                    docker-compose exec -T web python manage.py migrate
                """
            }
        }
    }

    post {
        success {
            echo 'Deployment successful! Application is running on port 8004.'
        }
        failure {
            echo 'Build or Deployment failed. Please check the logs above.'
        }
    }
}
