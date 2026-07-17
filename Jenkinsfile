pipeline {
    agent {
        kubernetes {
            defaultContainer 'kaniko'

            yaml '''
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

  volumes:
    - name: docker-config
      secret:
        secretName: docker-config
        items:
          - key: .dockerconfigjson
            path: config.json
'''
        }
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
                    sh '''
                    echo "Building Flask API..."

                    /kaniko/executor \
                      --context=${WORKSPACE}/api \
                      --dockerfile=${WORKSPACE}/api/Dockerfile \
                      --destination=hajlilahcen/flask-api:${BUILD_NUMBER} \
                      --destination=hajlilahcen/flask-api:latest \
                      --cache=true
                    '''
                }
            }
        }

        stage('Build Frontend') {
            steps {
                container('kaniko') {
                    sh '''
                    echo "Building Frontend..."

                    /kaniko/executor \
                      --context=${WORKSPACE}/frontend \
                      --dockerfile=${WORKSPACE}/frontend/Dockerfile \
                      --destination=hajlilahcen/bank-frontend:${BUILD_NUMBER} \
                      --destination=hajlilahcen/bank-frontend:latest \
                      --cache=true
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '===================================='
            echo ' Pipeline completed successfully!'
            echo ' Flask API pushed to Docker Hub'
            echo ' Frontend pushed to Docker Hub'
            echo '===================================='
        }

        failure {
            echo '===================================='
            echo ' Pipeline failed!'
            echo '===================================='
        }

        always {
            cleanWs()
        }
    }
}
