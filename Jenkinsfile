pipeline {

    agent {
        kubernetes {

            defaultContainer 'jnlp'

            yaml '''
apiVersion: v1
kind: Pod

spec:

  serviceAccountName: jenkins

  containers:

  - name: jnlp
    image: jenkins/inbound-agent

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

                sh 'pwd'

                sh 'whoami'

                container('busybox') {

                    sh 'echo HELLO FROM BUSYBOX'

                }

            }

        }

    }

}
