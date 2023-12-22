pipeline {
  agent any
  stages {
    stage("Setup environment") {
      steps {
        sh '''
        chmod +x jenkins-scripts/envsetup.sh
        ./jenkins-scripts/envsetup.sh
        '''
      }
    }
    stage("Setup Gunicorn") {
      steps {
        sh '''
        chmod +x jenkins-scripts/gunicorn.sh
        ./jenkins-scripts/gunicorn.sh
        '''
      }
    }
    stage("Setup NGINX") {
      steps {
        sh '''
        chmod +x jenkins-scripts/nginx.sh
        ./jenkins-scripts/nginx.sh
        '''
      }
    }
  }
}
