pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/singhprakash2324/ca2_377'
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
