variable "project_name" {
  description = "Project name used for secret naming."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "tags" {
  description = "Tags applied to resources."
  type        = map(string)
}
