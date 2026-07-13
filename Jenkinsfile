pipeline {
    agent {
        kubernetes {

            defaultContainer 'busybox'

            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: jenkins-agent
spec:
  serviceAccountName: jenkins

  containers:

  - name: busybox
    image: busybox:1.36
    command:
      - cat
    tty: true
'''
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {

                sh 'echo "===== Jenkins Kubernetes Agent ====="'
                sh 'hostname'
                sh 'whoami'
                sh 'pwd'

                container('busybox') {
                    sh 'echo "Repository content:"'
                    sh 'ls -la'
                }

            }
        }

    }

    post {
        always {
            echo "Pipeline finished successfully."
        }
    }
}
