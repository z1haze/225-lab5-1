pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE_FLASK = "cithit/hendris3-flask"
        DOCKER_IMAGE_REACT = "cithit/hendris3-react"
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/z1haze/225-lab5-1.git'
        KUBECONFIG = credentials('hendris3-225')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM', branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: "${env.GITHUB_URL}"]]
                ])
            }
        }

        stage('Build Flask Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE_FLASK}:${env.IMAGE_TAG}", "-f Dockerfile.flask .")
                }
            }
        }

        stage('Build React Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE_REACT}:${env.IMAGE_TAG}", "-f Dockerfile.react .")
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${env.DOCKER_CREDENTIALS_ID}") {
                        docker.image("${env.DOCKER_IMAGE_FLASK}:$IMAGE_TAG").push()
                        docker.image("${env.DOCKER_IMAGE_REACT}:$IMAGE_TAG").push()
                    }
                }
            }
        }

        stage('Deploy Flask App') {
            steps {
                script {
                    sh "sed -i 's|${env.DOCKER_IMAGE_FLASK}:latest|${env.DOCKER_IMAGE_FLASK}:${env.IMAGE_TAG}|' deployment-flask.yaml"
                    sh "cd .."
                    sh "kubectl apply -f deployment-flask.yaml"
                }
            }
        }

        stage('Deploy React App') {
            steps {
                script {
                    sh "sed -i 's|${env.DOCKER_IMAGE_REACT}:latest|${env.DOCKER_IMAGE_REACT}:${env.IMAGE_TAG}|' deployment-react.yaml"
                    sh "cd .."
                    sh "kubectl apply -f deployment-react.yaml"
                }
            }
        }
    }
}