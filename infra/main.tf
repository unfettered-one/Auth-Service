module "auth_service" {
  source = "github.com/unfettered-one/Infra//core?ref=fix/terraform-core"#TODO: change ref to tag after testing

  service_name = "auth-service"
  stage        = var.stage
  region       = var.region

  use_container = false
  use_zip       = true
  use_ecr       = false

  lambda_zip_path = "${path.module}/../auth_service.zip"
  lambda_handler  = "main.app"

  lambda_execution_policy_arn = var.lambda_execution_policy_arn
  environment_variables       = var.environment_variables

  create_http_api = false
  enable_dynamodb = false
}
