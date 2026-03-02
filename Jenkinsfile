pipeline {
    agent any

    environment {
        // Change these to your actual server details
        SERVER_IP = '72.60.219.145'
        SERVER_USER = 'root' // or your username
        DEPLOY_PATH = '/home/root/Analyatics' // Path where code will live on server
        SSH_CREDENTIAL_ID = 'hostinger-ssh-key' // ID of the SSH credential you create in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy to Hostinger') {
            steps {
                sshagent([env.SSH_CREDENTIAL_ID]) {
                    // 1. Create directory if not exists
                    sh "ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_IP} 'mkdir -p ${DEPLOY_PATH}'"
                    
                    // 2. Transfer files using rsync (fastest way)
                    // We exclude venv, .git, and local db files
                    sh "rsync -avz --exclude 'venv' --exclude '.git' --exclude 'db.sqlite3' ./ ${SERVER_USER}@${SERVER_IP}:${DEPLOY_PATH}"
                    
                    // 3. Restart Docker Containers on the server
                    sh """
                        ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_IP} "
                            cd ${DEPLOY_PATH} &&
                            docker-compose down &&
                            docker-compose up -d --build &&
                            docker-compose exec -T web python manage.py migrate
                        "
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed. Check logs.'
        }
    }
}
