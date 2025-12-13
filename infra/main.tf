module "auth_service" {
  source = "github.com/unfettered-one/Infra//core?ref=feat/lambda-url"

  service_name = "auth-service"
  stage        = var.stage
  region       = var.region

  use_container = true
  use_zip       = false
  use_ecr       = false

  lambda_image_uri = var.lambda_image_uri
  lambda_handler   = "auth_service.main.mangum_handler"

  lambda_execution_policy_arn = aws_iam_policy.lambda_dynamodb_policy.arn
  environment_variables       = {}

  create_http_api     = false
  enable_dynamodb     = true
  dynamodb_table_name = "auth-service-user-records-${var.stage}"
  gsi                 = "email-index"
  new_attribute       = "email"
}
