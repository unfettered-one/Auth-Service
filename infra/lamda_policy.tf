resource "aws_iam_policy" "lambda_dynamodb_policy" {
  name        = "${var.service_name}-lambda-dynamodb-policy-${var.stage}"
  description = "IAM policy for Lambda to access DynamoDB tables for ${var.service_name}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DynamoDBAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:*Item",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = "arn:aws:dynamodb:${var.region}:*:table/${var.service_name}-*"
      },
      {
        Sid    = "DynamoDBIndexAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = "arn:aws:dynamodb:${var.region}:*:table/${var.service_name}-*/index/*"
      }
    ]
  })

  tags = {
    Name        = "${var.service_name}-lambda-dynamodb-policy"
    Environment = var.stage
    Service     = var.service_name
  }
}

