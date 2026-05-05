pipeline {
  agent any

  options {
    timestamps()
    skipDefaultCheckout()
  }

  parameters {
    choice(name: 'DRY_RUN', choices: ['true', 'false'], description: 'Select true for terraform plan/destroy plan only, false to apply/destroy.')
    booleanParam(name: 'CREATE_EC2_INSTANCE', defaultValue: true, description: 'Create or destroy the EC2 instance module')
    booleanParam(name: 'CREATE_ELASTIC_IP', defaultValue: true, description: 'Create or destroy the Elastic IP module')
    booleanParam(name: 'CREATE_EBS_VOLUME', defaultValue: true, description: 'Create or destroy the EBS volume module')
    booleanParam(name: 'CREATE_SNAPSHOT', defaultValue: true, description: 'Create or destroy the Snapshot module')
  }

  environment {
    TF_DIR = 'terraform-project/terraform'
    SONAR_PROJECT_KEY = 'your-sonar-project-key'
    SONAR_HOST_URL = 'https://sonarcloud.io'
  }

  stages {
    stage('SCM Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Terraform Tool') {
      steps {
        script {
          env.TERRAFORM_CMD = isUnix() ? "${tool 'terraform'}/terraform" : "${tool 'terraform'}\\terraform.exe"
          echo "Using Terraform from: ${env.TERRAFORM_CMD}"
        }
      }
    }

    stage('Terraform Init') {
      steps {
        dir(env.TF_DIR) {
          script {
            if (isUnix()) {
              sh "\"${env.TERRAFORM_CMD}\" init -input=false"
            } else {
              bat "\"${env.TERRAFORM_CMD}\" init -input=false"
            }
          }
        }
      }
    }

    stage('Scans') {
      steps {
        dir(env.TF_DIR) {
          script {
            def trivyConfig = isUnix() ? 'trivy config --format json --output trivy-iac-report.json .' : 'trivy config --format json --output trivy-iac-report.json .'
            def trivyFs = isUnix() ? "trivy fs --format json --output ../trivy-fs-report.json .." : "trivy fs --format json --output ..\\trivy-fs-report.json .."

            echo 'Running Trivy IaC and filesystem scans...'
            if (isUnix()) {
              sh trivyConfig
              sh trivyFs
            } else {
              bat trivyConfig
              bat trivyFs
            }

            echo 'Optional Sonar scan: ensure sonar-scanner is installed and SONAR_TOKEN is configured.'
            if (env.SONAR_TOKEN) {
              def sonarCmd = isUnix() ? 'sonar-scanner -Dsonar.projectKey=' + env.SONAR_PROJECT_KEY + ' -Dsonar.host.url=' + env.SONAR_HOST_URL + ' -Dsonar.login=' + env.SONAR_TOKEN + ' -Dsonar.sources=.' : 'sonar-scanner -Dsonar.projectKey=' + env.SONAR_PROJECT_KEY + ' -Dsonar.host.url=' + env.SONAR_HOST_URL + ' -Dsonar.login=' + env.SONAR_TOKEN + ' -Dsonar.sources=.'
              if (isUnix()) {
                sh sonarCmd
              } else {
                bat sonarCmd
              }
            } else {
              echo 'Skipping Sonar scan because SONAR_TOKEN is not defined.'
            }
          }
        }
      }
    }

    stage('Create Resources') {
      when {
        expression { params.DRY_RUN == 'false' }
      }
      steps {
        script {
          def targets = []
          if (params.CREATE_EC2_INSTANCE) { targets.add('-target=module.ec2_instance') }
          if (params.CREATE_ELASTIC_IP) { targets.add('-target=module.elastic_ip') }
          if (params.CREATE_EBS_VOLUME) { targets.add('-target=module.ebs_volume') }
          if (params.CREATE_SNAPSHOT) { targets.add('-target=module.snapshot') }

          if (targets.isEmpty()) {
            error 'No resources selected for creation. Please enable at least one checkbox.'
          }

          dir(env.TF_DIR) {
            def targetArgs = targets.join(' ')
            def cmd = isUnix() ? "\"${env.TERRAFORM_CMD}\" apply -auto-approve ${targetArgs}" : "\"${env.TERRAFORM_CMD}\" apply -auto-approve ${targetArgs}"
            echo "Applying selected resources: ${targetArgs}"
            if (isUnix()) {
              sh cmd
            } else {
              bat cmd
            }
          }
        }
      }
    }

    stage('Plan Creation (Dry Run)') {
      when {
        expression { params.DRY_RUN == 'true' }
      }
      steps {
        script {
          def targets = []
          if (params.CREATE_EC2_INSTANCE) { targets.add('-target=module.ec2_instance') }
          if (params.CREATE_ELASTIC_IP) { targets.add('-target=module.elastic_ip') }
          if (params.CREATE_EBS_VOLUME) { targets.add('-target=module.ebs_volume') }
          if (params.CREATE_SNAPSHOT) { targets.add('-target=module.snapshot') }

          if (targets.isEmpty()) {
            error 'No resources selected for dry-run creation. Please enable at least one checkbox.'
          }

          dir(env.TF_DIR) {
            def targetArgs = targets.join(' ')
            def cmd = isUnix() ? "\"${env.TERRAFORM_CMD}\" plan ${targetArgs}" : "\"${env.TERRAFORM_CMD}\" plan ${targetArgs}"
            echo "Planning selected resource creation: ${targetArgs}"
            if (isUnix()) {
              sh cmd
            } else {
              bat cmd
            }
          }
        }
      }
    }

    stage('Delete Resources') {
      steps {
        script {
          def targets = []
          if (params.CREATE_EC2_INSTANCE) { targets.add('-target=module.ec2_instance') }
          if (params.CREATE_ELASTIC_IP) { targets.add('-target=module.elastic_ip') }
          if (params.CREATE_EBS_VOLUME) { targets.add('-target=module.ebs_volume') }
          if (params.CREATE_SNAPSHOT) { targets.add('-target=module.snapshot') }

          if (targets.isEmpty()) {
            error 'No resources selected for deletion. Please enable at least one checkbox.'
          }

          dir(env.TF_DIR) {
            def targetArgs = targets.join(' ')
            def cmd = params.DRY_RUN == 'true' ? "\"${env.TERRAFORM_CMD}\" plan -destroy ${targetArgs}" : "\"${env.TERRAFORM_CMD}\" destroy -auto-approve ${targetArgs}"
            echo "Executing resource deletion stage with dry-run=${params.DRY_RUN}: ${targetArgs}"
            if (isUnix()) {
              sh cmd
            } else {
              bat cmd
            }
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'terraform-project/terraform/trivy-iac-report.json, trivy-fs-report.json', allowEmptyArchive: true
    }
  }
}
