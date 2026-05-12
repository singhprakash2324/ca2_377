// Jenkinsfile
pipeline {
    agent any

    environment {
        APP_PORT = "8501"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/singhprakash2324/ca2_377'
            }
        }

        stage('Install Python & Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Application') {
            steps {
                sh 'nohup python3 app.py &'
            }
        }
    }

    post {
        success {
            echo 'Streamlit app deployed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}