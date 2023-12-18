pipeline {
  agent any
  stages {
    stage("Install dependencies") {
      sh '''
      pip install -r requirements/development.txt
      '''
    }
    stage("Setup Gunicorn") {
      steps {
        sh '''
        chmod +x guicorn.sh
        ./guicorn.sh
        '''
      }
    }
    stage("Setup NGINX") {
      steps {
        sh '''
        chmod +x nginx.sh
        ./nginx.sh
        '''
      }
    }
  }
}
