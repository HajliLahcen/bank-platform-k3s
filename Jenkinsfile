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

        GIT_REPO = "https://github.com/hajlilahcen/bank-platform-k3s.git"

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

                        sh """

                        git config --global user.email "jenkins@local"

                        git config --global user.name "Jenkins"

                        git add ${VALUES_FILE}

                        git diff --cached --quiet && exit 0

                        git commit -m "[skip ci] Update image tags to build ${BUILD_NUMBER}"

                        git remote set-url origin https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/hajlilahcen/bank-platform-k3s.git

                        git push origin HEAD:main

                        """

                    }

                }

            }

        }

    }

    post {

        success {

            echo "=============================================="

            echo "Build Successful"

            echo "API Image:"
            echo "${API_IMAGE}:${BUILD_NUMBER}"

            echo "Frontend Image:"
            echo "${FRONTEND_IMAGE}:${BUILD_NUMBER}"

            echo "Helm updated"

            echo "Git pushed"

            echo "ArgoCD will deploy automatically"

            echo "=============================================="

        }

        failure {

            echo "=============================================="

            echo "Pipeline Failed"

            echo "=============================================="

        }

        always {

            deleteDir()

        }

    }

}
