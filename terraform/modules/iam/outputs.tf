output "ci_role_arn" {
  description = "GitHub Actions CI role ARN."
  value       = aws_iam_role.ci.arn
}

output "cd_role_arn" {
  description = "GitHub Actions CD role ARN."
  value       = aws_iam_role.cd.arn
}

output "eks_cluster_role_arn" {
  description = "EKS cluster role ARN."
  value       = aws_iam_role.eks_cluster.arn
}

output "eks_node_role_arn" {
  description = "EKS managed node group role ARN."
  value       = aws_iam_role.eks_node.arn
}

output "github_oidc_provider_arn" {
  description = "GitHub Actions OIDC provider ARN."
  value       = aws_iam_openid_connect_provider.github_actions.arn
}
