pipeline {
    agent any

    environment {
        APP_PORT = "8501"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Install Python & Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Streamlit App') {
            steps {
                sh '''
                . venv/bin/activate

                nohup streamlit run app.py --server.port=$APP_PORT --server.address=0.0.0.0 > streamlit.log 2>&1 &
                '''
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