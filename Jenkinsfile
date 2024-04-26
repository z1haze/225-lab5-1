pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/hendris3'
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

        stage('Collect') {
            steps {
                script {
                    env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
                    env.GIT_AUTHOR = sh (script: 'git log -1 --pretty=%cn ${GIT_COMMIT}', returnStdout: true).trim()
                }
            }
        }

        stage('Lint') {
            steps {
                dir('client') {
                    sh 'npm install'
                    sh 'npm run lint'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}")
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${env.DOCKER_CREDENTIALS_ID}") {
                        docker.image("${env.DOCKER_IMAGE}:$IMAGE_TAG").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh "sed -i 's|${env.DOCKER_IMAGE}:latest|${env.DOCKER_IMAGE}:${env.IMAGE_TAG}|' prod-deployment.yaml"
                    sh "kubectl apply -f prod-deployment.yaml"
                }
            }
        }
    }

    post {
        success {
            slackSend color: "good", message: "Build Succeeded: ${env.JOB_NAME}-${env.BUILD_NUMBER} - ${env.GIT_COMMIT_MSG} by ${env.GIT_AUTHOR}"
        }

        unstable {
            slackSend color: "warning", message: "Build Finished: ${env.JOB_NAME}-${env.BUILD_NUMBER} - ${env.GIT_COMMIT_MSG} by ${env.GIT_AUTHOR}"
        }

        failure {
            slackSend color: "danger", message: "Build Failed: ${env.JOB_NAME}-${env.BUILD_NUMBER} - ${env.GIT_COMMIT_MSG} by ${env.GIT_AUTHOR}"
        }
    }
}