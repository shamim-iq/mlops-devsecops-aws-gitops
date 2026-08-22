locals {
  secret_paths = toset([
    for name in var.secret_names :
    "${var.project_name}/${var.environment}/${name}"
  ])
}

resource "aws_secretsmanager_secret" "this" {
  for_each = local.secret_paths

  name                    = each.value
  description             = "Empty secret container for ${var.project_name} ${var.environment}."
  recovery_window_in_days = 7

  tags = merge(var.tags, {
    Name = each.value
  })
}
