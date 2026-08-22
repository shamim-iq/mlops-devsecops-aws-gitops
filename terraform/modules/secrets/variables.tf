variable "project_name" {
  description = "Project name used for secret naming."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "secret_names" {
  description = "Secrets Manager secret path suffixes to create as empty containers."
  type        = list(string)
}

variable "tags" {
  description = "Tags applied to resources."
  type        = map(string)
}
