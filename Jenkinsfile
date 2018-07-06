pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Running tests'
                sh "pip install -r requirements.txt"
                sh "cd tests && pytest ."
            }
        }
        stage("Build"){
          steps {
            echo "hallais!"
            sh "ls -la"
          }
        }
    }
}
