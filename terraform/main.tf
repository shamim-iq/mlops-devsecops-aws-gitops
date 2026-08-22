module "networking" {
  source = "./modules/networking"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  tags                 = var.tags
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.ecr_repository_name
  tags            = var.tags
}

module "eks" {
  source = "./modules/eks"

  cluster_name               = var.eks_cluster_name
  cluster_role_arn           = module.iam.eks_cluster_role_arn
  cluster_security_group_ids = [module.networking.eks_cluster_security_group_id]
  subnet_ids                 = module.networking.private_subnet_ids
  node_role_arn              = module.iam.eks_node_role_arn
  node_instance_types        = var.eks_node_instance_types
  node_desired_size          = var.eks_node_desired_size
  node_min_size              = var.eks_node_min_size
  node_max_size              = var.eks_node_max_size
  tags                       = var.tags

  depends_on = [module.iam]
}

module "iam" {
  source = "./modules/iam"

  project_name       = var.project_name
  environment        = var.environment
  github_repository  = var.github_repository
  ecr_repository_arn = module.ecr.repository_arn
  tags               = var.tags
}

module "secrets" {
  source = "./modules/secrets"

  project_name = var.project_name
  environment  = var.environment
  secret_names = var.secret_names
  tags         = var.tags
}
