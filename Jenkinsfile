pipeline {
  agent any

  environment {
    DOCKERHUB_USER = 'vidernecic'
    TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDS = 'dockerhub-creds'
  }

  stages {
    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/vernecic/Vau_Konverter.git'
      }
    }

    stage('Build images') {
      steps {
        sh """
          docker build -t ${DOCKERHUB_USER}/vaukonverter-backend:${TAG} -t ${DOCKERHUB_USER}/vaukonverter-backend:latest backend
          docker build -t ${DOCKERHUB_USER}/vaukonverter-worker:${TAG}  -t ${DOCKERHUB_USER}/vaukonverter-worker:latest  worker
          docker build -t ${DOCKERHUB_USER}/vaukonverter-frontend:${TAG} -t ${DOCKERHUB_USER}/vaukonverter-frontend:latest front
        """
      }
    }

    stage('Push images') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh """
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin

            docker push ${DOCKERHUB_USER}/vaukonverter-backend:${TAG}
            docker push ${DOCKERHUB_USER}/vaukonverter-backend:latest

            docker push ${DOCKERHUB_USER}/vaukonverter-worker:${TAG}
            docker push ${DOCKERHUB_USER}/vaukonverter-worker:latest

            docker push ${DOCKERHUB_USER}/vaukonverter-frontend:${TAG}
            docker push ${DOCKERHUB_USER}/vaukonverter-frontend:latest
          """
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}
