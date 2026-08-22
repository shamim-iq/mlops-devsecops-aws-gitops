variable "aws_region" {
  description = "AWS region for demo-owned resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name used for demo resource naming."
  type        = string
  default     = "minimal-mlops-devsecops-pipeline"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "demo"
}

variable "vpc_cidr" {
  description = "CIDR block for the demo VPC."
  type        = string
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets."
  type        = list(string)
}

variable "ecr_repository_name" {
  description = "ECR repository name for the prediction API image."
  type        = string
}

variable "eks_cluster_name" {
  description = "EKS cluster name."
  type        = string
}

variable "eks_node_instance_types" {
  description = "CPU-only EKS managed node group instance types."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "eks_node_desired_size" {
  description = "Desired number of EKS worker nodes."
  type        = number
  default     = 1
}

variable "eks_node_min_size" {
  description = "Minimum number of EKS worker nodes."
  type        = number
  default     = 1
}

variable "eks_node_max_size" {
  description = "Maximum number of EKS worker nodes."
  type        = number
  default     = 1
}

variable "github_repository" {
  description = "GitHub repository allowed to assume CI/CD roles, in owner/name form."
  type        = string
}

variable "tags" {
  description = "Tags applied to demo-owned resources."
  type        = map(string)
  default = {
    Project     = "minimal-mlops-devsecops-pipeline"
    Environment = "demo"
    ManagedBy   = "terraform"
  }
}
