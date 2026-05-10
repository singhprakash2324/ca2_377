// Jenkinsfile
pipeline {
    agent any

    stages {


        // The repository is already cloned by Jenkins' SCM configuration.
        // No need for an explicit 'Clone Repository' stage here.

        stage('Build and Run Docker Containers') {
            steps {
                script {
                    // Stop and remove any previously running containers to ensure a clean start
                    sh 'docker-compose down || true'
                    // Build the Docker image for your Streamlit app
                    sh 'docker-compose build'
                    // Start the Docker containers in detached mode
                    sh 'docker-compose up -d'
                }
            }
        }
        // You can add more stages here, for example, to run tests on your Dockerized application
        // stage('Test Dockerized Application') {
        //     steps {
        //         script {
        //             // Example: Run tests inside the container
        //             // sh 'docker-compose exec web pytest'
        //         }
        //     }
        // }
    }
}