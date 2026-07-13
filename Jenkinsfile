pipeline {
    agent {
        kubernetes {

            defaultContainer 'busybox'

            podRetention(onFailure())

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

        stage('Environment') {
            steps {

                sh 'echo "===== Jenkins Kubernetes Agent ====="'
                sh 'hostname'
                sh 'whoami'
                sh 'pwd'

                container('busybox') {
                    sh 'echo "Hello from BusyBox!"'
                    sh 'uname -a'
                    sh 'ls -la'
                }

            }
        }

    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
