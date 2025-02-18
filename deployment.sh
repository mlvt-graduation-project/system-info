#!/bin/bash

# Configurable Variables
IMAGE_NAME="fastapi-app"
TAG="latest"
AWS_REGION="us-east-1"
ECR_REPO_NAME="fastapi-app-repo"
EC2_USER="ec2-user"
EC2_IP="your.ec2.instance.ip"
DOCKERFILE="Dockerfile"  # Adjust if your Dockerfile is in a subdirectory
APP_PORT=8000

# Ensure the script stops on errors
set -e

# 1. Build Docker Image
echo "Building Docker image..."
docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .

# 2. Tag the Docker Image
echo "Tagging Docker image for ECR..."
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME"
docker tag $IMAGE_NAME:$TAG $ECR_URI:$TAG

# 3. Authenticate Docker to AWS ECR
echo "Authenticating Docker to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

# 4. Push the Docker Image to ECR
echo "Pushing Docker image to ECR..."
aws ecr describe-repositories --repository-names $ECR_REPO_NAME || \
aws ecr create-repository --repository-name $ECR_REPO_NAME
docker push $ECR_URI:$TAG

# 5. SSH into EC2 and Deploy the Container
echo "Deploying Docker container to EC2..."
ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP << EOF
  set -e
  echo "Logging in to ECR..."
  aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

  echo "Pulling the latest image..."
  docker pull $ECR_URI:$TAG

  echo "Stopping and removing old container (if any)..."
  docker stop $IMAGE_NAME || true
  docker rm $IMAGE_NAME || true

  echo "Running the new container..."
  docker run -d --name $IMAGE_NAME -p $APP_PORT:$APP_PORT $ECR_URI:$TAG

  echo "Deployment complete. Container is running on port $APP_PORT."
EOF
