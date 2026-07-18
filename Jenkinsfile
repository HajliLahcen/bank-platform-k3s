pipeline {

    agent {
        kubernetes {

            defaultContainer 'kaniko'

            yaml """
apiVersion: v1
kind: Pod
spec:

  serviceAccountName: jenkins

  containers:

  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
      - /busybox/cat
    tty: true

    volumeMounts:
      - name: docker-config
        mountPath: /kaniko/.docker

  - name: tools
    image: hajlilahcen/jenkins-tools:1.0
    command:
      - cat
    tty: true

  volumes:
    - name: docker-config
      secret:
        secretName: docker-config
        items:
          - key: .dockerconfigjson
            path: config.json
"""
        }
    }

    environment {
        API_IMAGE = "hajlilahcen/flask-api"
        FRONTEND_IMAGE = "hajlilahcen/bank-frontend"
        VALUES_FILE = "helm/bank/values.yaml"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Flask API') {
            steps {
                container('kaniko') {
                    sh """
                    echo "Building Flask API..."

                    /kaniko/executor \
                      --context=${WORKSPACE}/api \
                      --dockerfile=${WORKSPACE}/api/Dockerfile \
                      --destination=${API_IMAGE}:${BUILD_NUMBER} \
                      --destination=${API_IMAGE}:latest \
                      --cache=true
                    """
                }
            }
        }

        stage('Build Frontend') {
            steps {
                container('kaniko') {
                    sh """
                    echo "Building Frontend..."

                    /kaniko/executor \
                      --context=${WORKSPACE}/frontend \
                      --dockerfile=${WORKSPACE}/frontend/Dockerfile \
                      --destination=${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                      --destination=${FRONTEND_IMAGE}:latest \
                      --cache=true
                    """
                }
            }
        }

        stage('Update Helm Values') {
            steps {
                container('tools') {
                    sh """
                    echo "Updating Helm values..."

                    yq -i '.api.image.tag="${BUILD_NUMBER}"' ${VALUES_FILE}
                    yq -i '.frontend.image.tag="${BUILD_NUMBER}"' ${VALUES_FILE}

                    echo "Updated values.yaml"
                    cat ${VALUES_FILE}
                    """
                }
            }
        }

        stage('Commit & Push') {
            steps {
                container('tools') {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-token',
                            usernameVariable: 'GIT_USERNAME',
                            passwordVariable: 'GIT_TOKEN'
                        )
                    ]) {

                        sh '''
                        set -e

                        echo "===== Configure Git ====="

                        git config --global --add safe.directory ${WORKSPACE}

                        git config --global user.email "ci@bank-platform.local"
                        git config --global user.name "Jenkins CI"

                        git status

                        echo "===== Add changes ====="

                        git add helm/bank/values.yaml

                        if git diff --cached --quiet; then
                            echo "No changes detected."
                            exit 0
                        fi

                        echo "===== Commit ====="

                        git commit -m "[skip ci] Update image tags to build ${BUILD_NUMBER}"

                        echo "===== Push ====="

                        git remote set-url origin https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/HajliLahcen/bank-platform-k3s.git

                        git push origin HEAD:main

                        echo "Push completed successfully."
                        '''
                    }
                }
            }
        }

    }

    post {

        success {

            echo "========================================"
            echo "Pipeline completed successfully!"
            echo "API Image: ${API_IMAGE}:${BUILD_NUMBER}"
            echo "Frontend Image: ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
            echo "Helm values updated"
            echo "GitHub updated"
            echo "ArgoCD will sync automatically"
            echo "========================================"

        }

        failure {

            echo "========================================"
            echo "Pipeline failed!"
            echo "========================================"

        }

        always {
            echo "Pipeline finished."
        }
    }
}
