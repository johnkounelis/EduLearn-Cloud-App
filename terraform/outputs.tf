output "aws_region" {
  description = "AWS region"
  value       = data.aws_region.current.name
}

output "account_id" {
  description = "AWS account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "backend_ecr_repository_url" {
  description = "Backend ECR repository URL"
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_repository_url" {
  description = "Frontend ECR repository URL"
  value       = aws_ecr_repository.frontend.repository_url
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = try(aws_lb.main[0].dns_name, "Not created")
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = try(aws_ecs_cluster.main[0].name, "Not created")
}

output "rds_endpoint" {
  description = "RDS database endpoint"
  value       = try(aws_db_instance.main[0].endpoint, "Not created")
  sensitive   = true
}