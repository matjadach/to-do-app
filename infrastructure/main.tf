terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "KPMG21_MateuszJadach_ProjectExercise"
    storage_account_name = "tfstatemodule12"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"

  }
}
provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "KPMG21_MateuszJadach_ProjectExercise"
}

resource "azurerm_storage_account" "tfstate" {
  name                     = "tfstatemodule12"
  resource_group_name      = data.azurerm_resource_group.main.name
  location                 = data.azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "blob"
}