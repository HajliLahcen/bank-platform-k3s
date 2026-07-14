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
'''
        }
    }

    stages {

        stage('Build Flask API') {
            steps {
                container('kaniko') {
                    sh '''
                    /kaniko/executor \
                      --context=$WORKSPACE \
                      --dockerfile=$WORKSPACE/api/Dockerfile \
                      --destination=hajlilahcen/flask-api:latest \
                      --cache=true
                    '''
                }
            }
        }

    }

    post {
        success {
            echo 'Flask API image successfully pushed to Docker Hub!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
