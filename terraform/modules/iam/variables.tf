variable "github_repository" {
  description = "GitHub repository allowed to assume CI/CD roles."
  type        = string
}

variable "ecr_repository_arn" {
  description = "ECR repository ARN."
  type        = string
  nullable    = true
}

variable "tags" {
  description = "Tags applied to resources."
  type        = map(string)
}
