pipeline {

    agent any

    environment {
        BASE_URL = 'https://restful-booker.herokuapp.com'
        TIMEOUT = '10'

        BOOKER_CREDS = credentials('booker-credentials')

        RH_USERNAME = "${BOOKER_CREDS_USR}"
        RH_PASSWORD = "${BOOKER_CREDS_PSW}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run API Tests') {
            steps {
                catchError(
                    buildResult: 'UNSTABLE',
                    stageResult: 'UNSTABLE'
                ) {
                    bat 'python -m pytest -v'
                }
            }
        }
    }

    post {

        always {
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'test-report.html',
                reportName: 'Pytest HTML Report'
            ])
        }
    }
}