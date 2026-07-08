pipeline {

    agent {
        label 'kaniko'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Show Workspace') {
            steps {
                sh '''
                pwd
                ls -R
                '''
            }
        }

        stage('Kaniko Test') {
            steps {
                container('kaniko') {
                    sh '''
                    echo "Running inside Kaniko"
                    /kaniko/executor version
                    '''
                }
            }
        }

    }

}
