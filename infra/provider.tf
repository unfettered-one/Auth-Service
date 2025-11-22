terraform {
  backend "s3" {
    bucket         = "${var.lock_bucket}"
    key            = "auth-service/terraform.tfstate"
    region         = "${var.region}"
    dynamodb_table = "${var.lock_table}"
    encrypt        = true
  }
}


provider "aws" {
  region = var.region

  default_tags {
    tags = {
      ManagedBy   = "UnfetteredOne"
      Environment = var.stage
      Service     = "auth-service"
    }
  }
}
