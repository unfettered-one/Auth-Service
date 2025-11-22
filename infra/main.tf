module "auth_service" {
  source = "github.com/unfettered-one/Infra//core?ref=main"

  service_name = "auth-service"
  stage        = var.stage
  region       = var.region

  use_container = true
  use_zip       = false
  use_ecr       = false

  lambda_image_uri            = var.lambda_image_uri
  lambda_execution_policy_arn = var.lambda_execution_policy_arn
  environment_variables       = var.environment_variables

  create_http_api = true
  enable_dynamodb = false
}
