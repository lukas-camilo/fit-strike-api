output "lambda_function_name" {
  value = aws_lambda_function.my_lambda.function_name
}

output "lambda_function_alias" {
  value = aws_lambda_alias.my_lambda_alias.name
}