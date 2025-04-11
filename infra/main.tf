provider "aws" {
  region = var.aws_region
}

terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket  = "terraform-state-bucket-lucas"
    key     = "terraform-fit-strike.tfstate"
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
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Função Lambda com versionamento
resource "aws_lambda_function" "my_lambda" {
  function_name    = "fit-strike-api"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  publish          = true
  s3_bucket        = var.s3_bucket_name
  s3_key           = var.s3_key
  source_code_hash = var.source_code_hash


  environment {
    variables = {
      ENV = "production"
    }
  }
}

# Alias para a versão publicada mais recente
resource "aws_lambda_alias" "my_lambda_alias" {
  name            = "live"
  function_name   = aws_lambda_function.my_lambda.function_name
  function_version = aws_lambda_function.my_lambda.version
}

output "lambda_function_arn" {
  value = aws_lambda_function.my_lambda.arn
}