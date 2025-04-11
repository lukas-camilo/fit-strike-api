variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "lambda_name" {
  description = "Nome da função lambda"
  type        = string
  default     = "fit-strike-api"
}