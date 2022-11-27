variable "flask_env" {}

variable "oauth_client_id" {
  sensitive = true
}
variable "oauth_client_secret" {
  sensitive = true
}
variable "admin_id" {
  sensitive = true
}

variable "tasks_db_name" {
  default = "tasks_db"
}

variable "tasks_collection_name" {
  default = "tasks_collection"
}

variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "flask_app" {
  default = "todo_app/app"
}

variable "secret_key" {
  sensitive = true
}

variable "loggly_token" {
  sensitive = true
}

variable "log_level" {
  default = "DEBUG"
}
