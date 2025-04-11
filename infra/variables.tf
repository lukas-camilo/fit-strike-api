variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "S3 bucket name for Lambda code"
  type        = string
}

variable "s3_key" {
  description = "S3 key for Lambda code"
  type        = string
}

variable "lambda_zip_path" {
  description = "Path to the Lambda zip file"
  type        = string
}

variable "source_code_hash" {
  description = "Hash do código fonte da Lambda"
  type        = string
}