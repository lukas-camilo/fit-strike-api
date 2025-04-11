provider "aws" {
  region = var.aws_region
}

terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket  = "terraform-state-bucket-lucas"
    key     = "terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

# Role para a Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Política para a Role
resource "aws_iam_role_policy" "lambda_policy" {
  name   = "lambda_policy"
  role   = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Função Lambda
resource "aws_lambda_function" "my_lambda" {
  function_name = "fit-strike-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler" # Formato: <arquivo>.<função>
  runtime       = "python3.9" # Substitua pela versão do Python desejada
  filename      = "lambda_function.zip" # Arquivo zip da função Lambda
  source_code_hash = filebase64sha256("lambda_function.zip")
  environment {
    variables = {
      ENV_VAR = "value" # Substitua por variáveis de ambiente necessárias
    }
  }
}

# Output para integração com o workflow
output "lambda_function_name" {
  value = aws_lambda_function.my_lambda.function_name
}