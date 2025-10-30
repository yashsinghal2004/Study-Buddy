pipeline {
    agent any
<<<<<<< HEAD
    environment {
        DOCKER_HUB_REPO = "yash9886/study-buddy"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
=======
>>>>>>> 16a7900e91e4872a36ff74c2f4941b7520866953
    stages {
        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/yashsinghal2004/Study-Buddy']])
            }
        }        
<<<<<<< HEAD
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }
        stage('Push Image to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    docker.withRegistry('https://registry.hub.docker.com' , "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }
        
    }
}
=======
    }
}
>>>>>>> 16a7900e91e4872a36ff74c2f4941b7520866953
