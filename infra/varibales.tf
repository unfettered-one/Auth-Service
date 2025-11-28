variable "stage" {
  default     = "dev"
  description = "The environment stage (e.g., dev, prod)"
  type        = string
}
variable "region" {
  default     = "ap-south-1"
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "lambda_execution_policy_arn" {
  type        = string
  description = "Policy ARN to attach to the Lambda role"
}

variable "service_name" {
  type    = string
  default = "auth-service"
}

variable "dynamodb_table_name" {
  type        = string
  description = "The name of the DynamoDB table"
}

variable "environment_variables" {
  description = "Envrionmet variables for lambda"
}

variable "lock_table" {
  type        = string
  description = "name of the state lock dynamodb table"
}

variable "lock_bucket" {
  type        = string
  description = "name of the state lock s3 bucket"
}

variable "lambda_image_uri" {
  description = "Docker image URI for Lambda function"
  type        = string
  default     = ""
}
