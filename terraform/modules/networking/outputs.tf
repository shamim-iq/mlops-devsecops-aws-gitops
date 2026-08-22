output "vpc_id" {
  description = "Demo VPC ID."
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs for load balancers and NAT."
  value       = values(aws_subnet.public)[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs for EKS."
  value       = values(aws_subnet.private)[*].id
}

output "eks_cluster_security_group_id" {
  description = "Additional security group ID attached to the EKS cluster."
  value       = aws_security_group.eks_cluster.id
}
