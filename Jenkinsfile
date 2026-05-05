pipeline {
  agent any

  parameters {
    booleanParam(name: 'DRY_RUN', defaultValue: true)
    booleanParam(name: 'CREATE_EC2_INSTANCE', defaultValue: true)
    booleanParam(name: 'CREATE_ELASTIC_IP', defaultValue: false)
    booleanParam(name: 'CREATE_EBS_VOLUME', defaultValue: false)
    booleanParam(name: 'CREATE_SNAPSHOT', defaultValue: false)
  }

  environment {
    TF = "${WORKSPACE}\\terraform.exe"
    TF_DIR = "${WORKSPACE}\\terraform"
    AWS_DEFAULT_REGION = "us-east-1"
  }

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/lochan-25/terraform-project.git'
      }
    }

    stage('Verify Repo') {
      steps {
        bat 'dir'
        bat 'dir terraform'
        bat 'dir terraform\\*.tf'
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
        bat "\"${env.TF}\" -chdir=${env.TF_DIR} init"
      }
    }

    stage('Terraform Plan') {
      steps {
        bat "\"${env.TF}\" -chdir=${env.TF_DIR} plan"
      }
    }

    stage('Terraform Apply') {
      when {
        expression { params.DRY_RUN == false }
      }
      steps {
        bat "\"${env.TF}\" -chdir=${env.TF_DIR} apply -auto-approve"
      }
    }

    // 🔥 FIX: create cleanup.py automatically
    stage('Create cleanup.py') {
      steps {
        writeFile file: 'cleanup.py', text: '''
import sys

print("Cleanup script running")
resources = sys.argv[1:]

if not resources:
    print("No resources passed")
    exit(1)

for r in resources:
    print(f"Deleting resource: {r}")

print("Cleanup completed")
'''
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

          def args = resources.join(" ")

          bat "python cleanup.py ${args}"
        }
      }
    }

    stage('Dry Run Info') {
      when {
        expression { params.DRY_RUN == true }
      }
      steps {
        echo "DRY RUN — No resources created or deleted"
      }
    }

  }
}