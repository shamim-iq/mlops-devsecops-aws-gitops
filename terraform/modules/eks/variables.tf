variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
}

variable "cluster_role_arn" {
  description = "IAM role ARN used by the EKS control plane."
  type        = string
}

variable "cluster_security_group_ids" {
  description = "Additional security group IDs attached to the EKS cluster."
  type        = list(string)
}

variable "subnet_ids" {
  description = "Subnet IDs used by EKS."
  type        = list(string)
}

variable "node_role_arn" {
  description = "IAM role ARN used by the EKS managed node group."
  type        = string
}

variable "node_instance_types" {
  description = "CPU-only managed node group instance types."
  type        = list(string)
}

variable "node_desired_size" {
  description = "Desired node count."
  type        = number
}

variable "node_min_size" {
  description = "Minimum node count."
  type        = number
}

variable "node_max_size" {
  description = "Maximum node count."
  type        = number
}

variable "tags" {
  description = "Tags applied to resources."
  type        = map(string)
}
