output "vpc_id" {
  description = "Demo VPC ID."
  value       = module.networking.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnet IDs used by EKS."
  value       = module.networking.private_subnet_ids
}

output "ecr_repository_url" {
  description = "Prediction API ECR repository URL."
  value       = module.ecr.repository_url
}

output "eks_cluster_name" {
  description = "EKS cluster name."
  value       = module.eks.cluster_name
}

output "ci_role_arn" {
  description = "IAM role ARN for GitHub Actions CI."
  value       = module.iam.ci_role_arn
}
