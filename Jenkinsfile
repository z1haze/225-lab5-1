pipeline {
    agent any

    tools {
        nodejs '18.20.2'
    }

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

                script {
                    env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
                }
            }
        }

        stage('Lint & Test') {
            steps {
                dir('client') {
                    sh 'node -v'
                    sh 'npm install'
                    sh 'npm run lint'
                    sh 'npm test'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}:${env.IMAGE_TAG}", "-f Dockerfile.combo .")
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

        stage('Deploy Dev') {
            steps {
                script {
                    sh "sed -i 's|${env.DOCKER_IMAGE}:latest|${env.DOCKER_IMAGE}:${env.IMAGE_TAG}|' dev-deployment.yaml"
                    sh "kubectl apply -f dev-deployment.yaml"
                }
            }
        }

        stage("Run Live Tests") {
            steps {
                script {
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                    sh 'docker build -t qa-tests -f Dockerfile.test .'
                    sh 'docker run qa-tests'
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                }
            }
        }

        stage ("Run Security Checks") {
            steps {
                sh 'docker pull public.ecr.aws/portswigger/dastardly:latest'
                sh '''
                    docker run --user $(id -u) -v ${WORKSPACE}:${WORKSPACE}:rw \
                    -e BURP_START_URL=http://10.48.10.163 \
                    -e BURP_REPORT_FILE_PATH=${WORKSPACE}/dastardly-report.xml \
                    public.ecr.aws/portswigger/dastardly:latest
                '''
            }
        }

        stage('Deploy Prod') {
            steps {
                script {
                    sh "sed -i 's|${env.DOCKER_IMAGE}:latest|${env.DOCKER_IMAGE}:${env.IMAGE_TAG}|' prod-deployment.yaml"
                    sh "kubectl apply -f prod-deployment.yaml"
                }
            }
        }

        stage('Remove Test Data') {
            steps {
                script {
                    // Run the python script to generate data to add to the database
                    def appPod = sh(script: "kubectl get pods -l app=api -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- python3 data-reset.py"
                }
            }
        }

        stage('Check Kubernetes Cluster') {
            steps {
                script {
                    sh "kubectl get all"
                }
            }
        }
    }

    post {
        always {
            junit testResults: 'dastardly-report.xml', skipPublishingChecks: true
        }

        success {
            slackSend color: "good", message: "Build Succeeded: ${env.JOB_NAME}-${env.BUILD_NUMBER} - ${env.GIT_COMMIT_MSG}"
        }

        unstable {
            slackSend color: "warning", message: "Build Finished: ${env.JOB_NAME}-${env.BUILD_NUMBER} - ${env.GIT_COMMIT_MSG}"
        }

        failure {
            slackSend color: "danger", message: "Build Failed: ${env.JOB_NAME}-${env.BUILD_NUMBER} - ${env.GIT_COMMIT_MSG}"
        }
    }
}