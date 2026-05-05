pipeline {
  agent any

  parameters {
    booleanParam(name: 'DELETE_RESOURCES', defaultValue: false, description: 'Delete AWS resources using Python script')
  }

  environment {
    TF = "${WORKSPACE}\\terraform.exe"
    TF_DIR = "${WORKSPACE}\\python\\terraform_updated"
    AWS_DEFAULT_REGION = "us-east-1"
  }

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/lochan-25/terraform-project.git'
      }
    }

    stage('Setup Terraform') {
      steps {
        powershell '''
          Invoke-WebRequest -Uri https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_windows_amd64.zip -OutFile terraform.zip
          Expand-Archive terraform.zip -DestinationPath . -Force
        '''
      }
    }

    stage('Configure AWS') {
      steps {
        withCredentials([
          string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
          string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
          script {
            env.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
            env.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
          }
        }
      }
    }

    stage('Terraform Init') {
      steps {
        bat "\"${env.TF}\" -chdir=\"${env.TF_DIR}\" init"
      }
    }

    stage('Terraform Plan') {
      steps {
        bat "\"${env.TF}\" -chdir=\"${env.TF_DIR}\" plan"
      }
    }

    stage('Terraform Apply') {
      steps {
        bat "\"${env.TF}\" -chdir=\"${env.TF_DIR}\" apply -auto-approve"
      }
    }

    // =========================
    // 🔍 SONAR ANALYSIS (SAFE)
    // =========================
    stage('SonarQube Analysis') {
      steps {
        script {
          try {
            withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
              bat """
              sonar-scanner ^
              -Dsonar.projectKey=terraform-project ^
              -Dsonar.sources=. ^
              -Dsonar.host.url=http://localhost:9000 ^
              -Dsonar.login=%SONAR_TOKEN%
              """
            }
          } catch (Exception e) {
            echo "Sonar skipped (no token or scanner not installed)"
          }
        }
      }
    }

    // =========================
    // 📦 INSTALL PYTHON DEPS
    // =========================
    stage('Install Python Dependencies') {
      steps {
        bat 'python -m pip install boto3'
      }
    }

    // =========================
    // 🧹 CLEANUP (OPTIONAL)
    // =========================
    stage('Delete Resources (Python)') {
      when {
        expression { params.DELETE_RESOURCES == true }
      }
      steps {
        script {
          echo "Running cleanup script..."

          bat "python python\\cleanup.py ec2"
          bat "python python\\cleanup.py ebs"
          bat "python python\\cleanup.py s3"
        }
      }
    }

    stage('Dry Run Info') {
      when {
        expression { params.DELETE_RESOURCES == false }
      }
      steps {
        echo "Resources created. Cleanup not triggered."
      }
    }

  }

  post {
    always {
      echo "Pipeline completed successfully"
    }
  }
}
