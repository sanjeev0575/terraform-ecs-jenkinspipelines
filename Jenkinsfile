pipeline {
    agent any

    environment {
        AWS_REGION       = 'us-east-1'
        AWS_ACCOUNT_ID   = '115456585578'   // change to your AWS account ID
        ECR_REPOSITORY   = 'my-ecs-app'     // change to your ECR repo name
        ECR_REGISTRY     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG        = "build-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        cd simple-application
                        echo "Building Docker image..."
                        docker build -t ${ECR_REPOSITORY}:${IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} \
                          | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                script {
                    sh """
                        docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                        docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Terraform Init & Plan') {
            steps {
                sh """
                    cd terraform
                    terraform init -input=false
                    terraform plan -var-file=dev.tfvars \
                        -var "docker_image=${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}" \
                        -out=tfplan
                """
            }
        }

        stage('Terraform Apply') {
            steps {
                sh """
                    cd terraform
                    terraform apply -auto-approve tfplan
                """
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
