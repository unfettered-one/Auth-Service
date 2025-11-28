terraform {
  backend "s3" {
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

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
      configuration_aliases = [ aws ]
    }
  }
}
