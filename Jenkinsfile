pipeline {
  agent any

  environment {
    TF = "${WORKSPACE}\\terraform.exe"
    TF_DIR = "${WORKSPACE}\\terraform_updated"
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

  }
}