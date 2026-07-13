pipeline {
    agent {
        kubernetes {
            defaultContainer 'busybox'
            yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: busybox
    image: busybox
    command:
    - cat
    tty: true
'''
        }
    }

    stages {
        stage('Test') {
            steps {
                sh 'hostname'

                container('busybox') {
                    sh 'echo HELLO FROM BUSYBOX'
                }
            }
        }
    }
}
