output "secret_arns" {
  description = "Secret ARNs created for the demo."
  value       = [for secret in aws_secretsmanager_secret.this : secret.arn]
}
