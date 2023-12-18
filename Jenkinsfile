pipeline {
  agent any
  stages {
    stage("Setup environment") {
      steps {
        sh '''
        chmod +x envsetup.sh
        ./envsetup.sh
        '''
      }
    }
    stage("Setup Gunicorn") {
      steps {
        sh '''
        chmod +x gunicorn.sh
        ./gunicorn.sh
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
