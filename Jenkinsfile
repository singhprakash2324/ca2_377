pipeline {
    agent any


    stages {
        stage('Build') {
            steps {
                echo 'Stage 1: Building the project...'
                echo 'Compiling source code...'
                sh 'sleep 1'
                echo 'Build complete!'
            }
        }


        stage('Test') {
            steps {
                echo 'Stage 2: Running automated tests...'
                sh 'sleep 1'
                echo 'All tests passed!'
            }
        }


        stage('Deploy') {
            steps {
                echo 'Stage 3: Deploying to server...'
                sh 'sleep 1'
                echo 'Deployment successful!'
            }
        }
    }


    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check the logs.'
        }
    }
}