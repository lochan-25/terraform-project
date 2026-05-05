pipeline {
  agent any

  environment {
    TF = "${WORKSPACE}\\terraform.exe"
    TF_DIR = "terraform-project/terraform"
  }

  parameters {
    booleanParam(name: 'DRY_RUN', defaultValue: true)
    booleanParam(name: 'CREATE_EC2_INSTANCE', defaultValue: true)
    booleanParam(name: 'CREATE_ELASTIC_IP', defaultValue: false)
    booleanParam(name: 'CREATE_EBS_VOLUME', defaultValue: false)
    booleanParam(name: 'CREATE_SNAPSHOT', defaultValue: false)
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
          Expand-Archive -Path terraform.zip -DestinationPath . -Force
        '''
      }
    }

    stage('Terraform Init') {
      steps {
        bat "\"${env.TF}\" -chdir=${env.TF_DIR} init"
      }
    }

    stage('Plan (Dry Run)') {
      when {
        expression { params.DRY_RUN == true }
      }
      steps {
        script {
          def targets = []

          if (params.CREATE_EC2_INSTANCE) targets.add('-target=module.ec2_instance')
          if (params.CREATE_ELASTIC_IP) targets.add('-target=module.elastic_ip')
          if (params.CREATE_EBS_VOLUME) targets.add('-target=module.ebs_volume')
          if (params.CREATE_SNAPSHOT) targets.add('-target=module.snapshot')

          def targetArgs = targets.join(' ')

          bat "\"${env.TF}\" -chdir=${env.TF_DIR} plan ${targetArgs}"
        }
      }
    }

    stage('Apply') {
      when {
        expression { params.DRY_RUN == false }
      }
      steps {
        script {
          def targets = []

          if (params.CREATE_EC2_INSTANCE) targets.add('-target=module.ec2_instance')
          if (params.CREATE_ELASTIC_IP) targets.add('-target=module.elastic_ip')
          if (params.CREATE_EBS_VOLUME) targets.add('-target=module.ebs_volume')
          if (params.CREATE_SNAPSHOT) targets.add('-target=module.snapshot')

          def targetArgs = targets.join(' ')

          bat "\"${env.TF}\" -chdir=${env.TF_DIR} apply -auto-approve ${targetArgs}"
        }
      }
    }

    stage('Destroy') {
      steps {
        script {
          def targets = []

          if (params.CREATE_EC2_INSTANCE) targets.add('-target=module.ec2_instance')
          if (params.CREATE_ELASTIC_IP) targets.add('-target=module.elastic_ip')
          if (params.CREATE_EBS_VOLUME) targets.add('-target=module.ebs_volume')
          if (params.CREATE_SNAPSHOT) targets.add('-target=module.snapshot')

          def targetArgs = targets.join(' ')

          if (params.DRY_RUN) {
            bat "\"${env.TF}\" -chdir=${env.TF_DIR} plan -destroy ${targetArgs}"
          } else {
            bat "\"${env.TF}\" -chdir=${env.TF_DIR} destroy -auto-approve ${targetArgs}"
          }
        }
      }
    }

  }
}