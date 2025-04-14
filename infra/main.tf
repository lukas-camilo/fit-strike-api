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
resource "aws_iam_role_policy" "dynamodb_policy" {
  name = "lambda_dynamodb_policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.users_table.arn
      }
    ]
  })
}

# Tabela DynamoDB
resource "aws_dynamodb_table" "users_table" {
  name           = "users"
  billing_mode   = "PAY_PER_REQUEST" # Modo de pagamento por demanda
  hash_key       = "id"             # Chave primária

  attribute {
    name = "id"
    type = "S" # Tipo de dado: String
  }

  tags = {
    Environment = "Production"
    Name        = "UsersTable"
  }
}

# Função Lambda com versionamento
resource "aws_lambda_function" "my_lambda" {
  function_name = var.lambda_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  filename      = "../lambda_function.zip"

  environment {
    variables = {
      ENV          = "production"
      DYNAMODB_TABLE = aws_dynamodb_table.users_table.name
    }
  }
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id = "AllowAPIGatewayInvoke"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "arn:aws:apigateway:us-east-1::/restapis/q28uzvnoj1/*/*"
}