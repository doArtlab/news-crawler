VERSION=$(date +"%Y%m%d%H%M%S")
NAMESPACE=cosmax-crawler
IMAGE_NAME=news-crawler
ECR_URI=270500201376.dkr.ecr.ap-northeast-2.amazonaws.com/$NAMESPACE
ECR_REPO=$ECR_URI/$IMAGE_NAME

docker build --platform linux/amd64 -t $IMAGE_NAME:$VERSION .
docker tag $IMAGE_NAME:$VERSION $ECR_REPO:$VERSION

aws ecr get-login-password --region ap-northeast-2 --profile artlab | docker login --username AWS --password-stdin $ECR_URI
docker push $ECR_REPO:$VERSION

SSM_ARN=arn:aws:ssm:ap-northeast-2:270500201376:parameter/cosmax

aws ecs register-task-definition \
  --profile artlab \
  --region ap-northeast-2 \
  --family $NAMESPACE-$IMAGE_NAME \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --cpu "256" \
  --memory "512" \
  --execution-role-arn arn:aws:iam::270500201376:role/ecsTaskExecutionRole \
  --container-definitions "[ \
    { \
      \"name\": \"$IMAGE_NAME\", \
      \"image\": \"$ECR_REPO:$VERSION\", \
      \"environment\": [ \
        { \
          \"name\": \"APP_ENV\", \
          \"value\": \"development\" \
        } \
      ], \
      \"secrets\": [ \
        { \
          \"name\": \"OPENAI_API_KEY\", \
          \"valueFrom\": \"$SSM_ARN/openai/apiKey\" \
        }, \
        { \
          \"name\": \"GOOGLE_SEARCH_API_KEY\", \
          \"valueFrom\": \"$SSM_ARN/google/search/apiKey\" \
        }, \
         { \
          \"name\": \"GOOGLE_SEARCH_CX\", \
          \"valueFrom\": \"$SSM_ARN/google/search/cx\" \
        }, \
            { \
          \"name\": \"SUPABASE_URL\", \
          \"valueFrom\": \"$SSM_ARN/supabase/url\" \
        }, \
            { \
          \"name\": \"SUPABASE_SERVICE_ROLE_KEY\", \
          \"valueFrom\": \"$SSM_ARN/supabase/roleKey\" \
        } \
      ], \
      \"logConfiguration\": { \
        \"logDriver\": \"awslogs\", \
        \"options\": { \
          \"awslogs-group\": \"/ecs/$NAMESPACE/$IMAGE_NAME\", \
          \"awslogs-region\": \"ap-northeast-2\", \
          \"awslogs-stream-prefix\": \"ecs\" \
        } \
      } \
    } \
  ]"

