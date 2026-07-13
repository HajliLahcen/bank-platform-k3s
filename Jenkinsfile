pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: busybox
    image: busybox:1.36
    command:
      - cat
    tty: true
'''
            defaultContainer 'busybox'
        }
    }

    stages {
        stage('Environment') {
            steps {
                sh 'echo "===== POD INFO ====="'
                sh 'hostname'
                sh 'whoami'
                sh 'pwd'
                sh 'kubectl version --client || true'
                sh 'echo "Pipeline is running inside Kubernetes!"'
            }
        }
    }
}
