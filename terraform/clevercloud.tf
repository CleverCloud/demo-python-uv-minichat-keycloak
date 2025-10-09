terraform {
  required_version = ">= 1.5.0"
  required_providers {
    clevercloud = {
      source  = "CleverCloud/clevercloud"
      version = ">= 1.2.0"
    }
  }
}

# Provider configured with target organization
provider "clevercloud" {
  organisation = "ORGANISATION ID"
}

variable "region" {
  description = "Region slug (e.g., par for Paris, mtl for Montreal)."
  type        = string
  default     = "par"
}

# --- PG Database ---
resource "clevercloud_postgresql" "minichat_postgresql" {
  name   = "minichat_postgresql"
  region = var.region
  plan   = "xs_sml"
  version = "17"
}

# --- Python app ---
resource "clevercloud_python" "minichat_python" {
  name   = "minichat_python"
  region = var.region

  # Autoscaling configuration
  min_instance_count = 1
  max_instance_count = 10
  smallest_flavor    = "S"
  biggest_flavor     = "S"

  # Link to PostgreSQL 
  dependencies = [
    clevercloud_postgresql.minichat_postgresql.id,
  ]

  # GitHub repo deployment
  deployment {
    repository = "https://github.com/CleverCloud/demo-python-uv-minichat-keycloak.git"
  }

  # Environment variables
  environment = {
    "CC_PYTHON_VERSION"="3.13"
    "CC_RUN_COMMAND"="uv run main.py"
  }
}

# Outputs
output "clevercloud_python_app_id" {
  value = clevercloud_python.minichat_python.id
}

output "clevercloud_postgresql_id" {
  value = clevercloud_postgresql.minichat_postgresql.id
}