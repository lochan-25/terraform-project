pipeline {
  agent any

  environment {
    TF = "${WORKSPACE}\\terraform.exe"
  }

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        git branch: 'main', url: 'https://github.com/lochan-25/terraform-project.git'
      }
    }

    stage('Verify Repo Content') {
      steps {
        script {
          echo "Listing workspace files..."
          bat 'dir'
          bat 'dir /s'

          def tfFiles = bat(script: 'dir /s /b *.tf', returnStdout: true).trim()

          if (!tfFiles) {
            error "❌ No .tf files found. Repo checkout is wrong OR files not in repo root."
          }

          echo "✅ Terraform files found:\n${tfFiles}"

          def firstFile = tfFiles.split("\n")[0]
          def tfDir = firstFile.substring(0, firstFile.lastIndexOf("\\"))

          echo "📁 Terraform directory: ${tfDir}"
          env.TF_DIR = tfDir
        }
      }
    }

    stage('Setup Terraform') {
      steps {
        powershell '''
          Invoke-WebRequest -Uri https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_windows_amd64.zip -OutFile terraform.zip
          Expand-Archive -Path terraform.zip -DestinationPath . -Force
        '''
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

    stage('Terraform Destroy (Optional)') {
      when {
        expression { false } // keep disabled
      }
      steps {
        bat "\"${env.TF}\" -chdir=\"${env.TF_DIR}\" destroy -auto-approve"
      }
    }
  }
}