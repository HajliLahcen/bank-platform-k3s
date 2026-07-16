pipeline {

    agent {
        kubernetes {
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

    environment {
        REGISTRY = "hajlilahcen"
        IMAGE = "flask-api"
        TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker Config') {
            steps {
                container('kaniko') {
                    sh '''
                    echo "===== Docker config ====="
                    ls -la /kaniko/.docker

                    echo ""
                    echo "===== config.json ====="
                    cat /kaniko/.docker/config.json
                    '''
                }
            }
        }

        stage('Build & Push') {

            steps {

                container('kaniko') {

                    sh '''
                    /kaniko/executor \
                      --context=$WORKSPACE \
                      --dockerfile=$WORKSPACE/api/Dockerfile \
                      --destination=$REGISTRY/$IMAGE:$TAG \
                      --cache=true
                    '''
                }

            }

        }

    }

    post {

        success {
            echo "Docker image pushed successfully!"
        }

        failure {
            echo "Pipeline failed!"
        }

    }

}
