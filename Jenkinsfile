pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "haseeb67786/hakibank:latest"
        COMPOSE_FILE = "docker-compose.jenkins.yml"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Khawaja-Muhammad-Haseeb/Haki-Bank-.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose -f $COMPOSE_FILE down || true'
                sh 'docker compose -f $COMPOSE_FILE up -d'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
