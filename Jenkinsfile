pipeline {
  agent any
  environment {
    PATH = "/usr/bin:$PATH"
  }
  stages {
    stage("Setup Environment") {
      steps {
        script {
          sh '''
          chmod +x jenkins-scripts/envsetup.sh
          ./jenkins-scripts/envsetup.sh
          '''
        }
      }
    }
    stage("Setup Gunicorn") {
      steps {
        script {
          sh '''
          chmod +x jenkins-scripts/gunicorn.sh
          ./jenkins-scripts/gunicorn.sh
          '''
        }
      }
    }
    stage("Setup NGINX") {
      steps {
        script {
          sh '''
          chmod +x jenkins-scripts/nginx.sh
          ./jenkins-scripts/nginx.sh
          '''
        }
      }
    }
  }
}
  // post {
  //     success {
  //       slackSend(
  //         color: "good",
  //         message: "Build deployed successfully - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
  //       )
  //     }
  //     failure {
  //       slackSend(
  //         failOnError: true,
  //         color: "danger",
  //         message: "Build failed - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
  //       )
  //     }
  //   }
// }
