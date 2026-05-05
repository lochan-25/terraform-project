pipeline {
  agent any

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
        script {
          def tf = "${env.WORKSPACE}\\terraform.exe"
          bat "\"${tf}\" init"
        }
      }
    }

    stage('Plan Creation (Dry Run)') {
      when {
        expression { params.DRY_RUN == true }
      }
      steps {
        script {
          def tf = "${env.WORKSPACE}\\terraform.exe"

          def targets = []
          if (params.CREATE_EC2_INSTANCE) targets.add('-target=module.ec2_instance')
          if (params.CREATE_ELASTIC_IP) targets.add('-target=module.elastic_ip')
          if (params.CREATE_EBS_VOLUME) targets.add('-target=module.ebs_volume')
          if (params.CREATE_SNAPSHOT) targets.add('-target=module.snapshot')

          def targetArgs = targets.join(' ')
          bat "\"${tf}\" plan ${targetArgs}"
        }
      }
    }

    stage('Create Resources') {
      when {
        expression { params.DRY_RUN == false }
      }
      steps {
        script {
          def tf = "${env.WORKSPACE}\\terraform.exe"

          def targets = []
          if (params.CREATE_EC2_INSTANCE) targets.add('-target=module.ec2_instance')
          if (params.CREATE_ELASTIC_IP) targets.add('-target=module.elastic_ip')
          if (params.CREATE_EBS_VOLUME) targets.add('-target=module.ebs_volume')
          if (params.CREATE_SNAPSHOT) targets.add('-target=module.snapshot')

          def targetArgs = targets.join(' ')
          def tf = "${env.WORKSPACE}\\terraform.exe"
          bat "\"${tf}\" -chdir=terraform-project plan ${targetArgs}"
          bat "\"${tf}\" -chdir=terraform-project apply -auto-approve ${targetArgs}"
          bat "\"${tf}\" -chdir=terraform-project destroy -auto-approve ${targetArgs}"
        }
      }
    }

    stage('Delete Resources') {
      steps {
        script {
          def tf = "${env.WORKSPACE}\\terraform.exe"

          def targets = []
          if (params.CREATE_EC2_INSTANCE) targets.add('-target=module.ec2_instance')
          if (params.CREATE_ELASTIC_IP) targets.add('-target=module.elastic_ip')
          if (params.CREATE_EBS_VOLUME) targets.add('-target=module.ebs_volume')
          if (params.CREATE_SNAPSHOT) targets.add('-target=module.snapshot')

          def targetArgs = targets.join(' ')

          if (params.DRY_RUN) {
            bat "\"${tf}\" plan -destroy ${targetArgs}"
          } else {
            bat "\"${tf}\" destroy -auto-approve ${targetArgs}"
          }
        }
      }
    }
  }
}