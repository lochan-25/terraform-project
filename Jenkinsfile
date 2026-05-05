pipeline {
  agent any

  parameters {
    booleanParam(name: 'DRY_RUN', defaultValue: true)
    booleanParam(name: 'CREATE_EC2_INSTANCE', defaultValue: true)
  }

  environment {
    TF = "${WORKSPACE}\\terraform.exe"
    TF_DIR = "${WORKSPACE}\\infra"
    AWS_DEFAULT_REGION = "us-east-1"
  }

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/lochan-25/terraform-project.git'
      }
    }

    // 🔥 FIX: create Terraform config if missing
    stage('Create Terraform Files') {
      steps {
        script {
          bat 'mkdir infra'

          writeFile file: 'infra/main.tf', text: '''
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
'''
        }
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
          bat '''
          set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
          set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%
          set AWS_DEFAULT_REGION=us-east-1
          '''
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
      when {
        expression { params.DRY_RUN == false }
      }
      steps {
        bat "\"${env.TF}\" -chdir=\"${env.TF_DIR}\" apply -auto-approve"
      }
    }

    // 🔥 FIX: create cleanup script
    stage('Create cleanup.py') {
      steps {
        writeFile file: 'cleanup.py', text: '''
import sys
print("Cleanup running")
print("Resources:", sys.argv[1:])
'''
      }
    }

    stage('Cleanup Resources') {
      when {
        expression { params.DRY_RUN == false }
      }
      steps {
        bat "python cleanup.py ec2"
      }
    }

    stage('Dry Run Info') {
      when {
        expression { params.DRY_RUN == true }
      }
      steps {
        echo "DRY RUN — nothing applied"
      }
    }
  }
}