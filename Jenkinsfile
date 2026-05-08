pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'YOUR_GITHUB_REPO'
            }
        }

        stage('Install Dependencies') {
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
}