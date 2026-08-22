variable "project_name" {
  description = "Project name used for role naming."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "github_repository" {
  description = "GitHub repository allowed to assume CI/CD roles."
  type        = string
}

variable "ecr_repository_arn" {
  description = "ECR repository ARN."
  type        = string
}

variable "tags" {
  description = "Tags applied to resources."
  type        = map(string)
}
