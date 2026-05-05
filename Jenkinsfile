pipeline {
  agent any

  parameters {
    booleanParam(name: 'DRY_RUN', defaultValue: true, description: 'If true, only simulate. If false, cleanup runs.')
    booleanParam(name: 'CREATE_EC2_INSTANCE', defaultValue: true)
    booleanParam(name: 'CREATE_ELASTIC_IP', defaultValue: false)
    booleanParam(name: 'CREATE_EBS_VOLUME', defaultValue: false)
    booleanParam(name: 'CREATE_SNAPSHOT', defaultValue: false)
  }

  environment {
    SONAR_PROJECT_KEY = "terraform-project"
    SONAR_HOST_URL = "http://localhost:9000"   // change if needed
  }

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/lochan-25/terraform-project.git'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          echo "Starting Sonar analysis..."

          try {
            withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
              bat """
              sonar-scanner ^
                -Dsonar.projectKey=${env.SONAR_PROJECT_KEY} ^
                -Dsonar.host.url=${env.SONAR_HOST_URL} ^
                -Dsonar.login=%SONAR_TOKEN% ^
                -Dsonar.sources=.
              """
            }
          } catch (Exception e) {
            echo "⚠️ Sonar credentials not found OR scanner not installed. Skipping Sonar."
          }
        }
      }
    }

    stage('Show Sonar Report') {
      steps {
        echo "👉 Sonar Dashboard: ${env.SONAR_HOST_URL}/dashboard?id=${env.SONAR_PROJECT_KEY}"
      }
    }

    stage('Cleanup Resources (Python)') {
      when {
        expression { params.DRY_RUN == false }
      }
      steps {
        script {

          def resources = []

          if (params.CREATE_EC2_INSTANCE) resources.add("ec2")
          if (params.CREATE_ELASTIC_IP) resources.add("eip")
          if (params.CREATE_EBS_VOLUME) resources.add("ebs")
          if (params.CREATE_SNAPSHOT) resources.add("snapshot")

          if (resources.isEmpty()) {
            error "❌ No resources selected for cleanup"
          }

          def resourceArgs = resources.join(" ")

          echo "Deleting resources: ${resourceArgs}"

          bat "python cleanup.py ${resourceArgs}"
        }
      }
    }

    stage('Dry Run Info') {
      when {
        expression { params.DRY_RUN == true }
      }
      steps {
        echo "✅ DRY RUN ENABLED — No resources will be deleted"
      }
    }

  }

  post {
    always {
      echo "Pipeline completed"
    }
  }
}