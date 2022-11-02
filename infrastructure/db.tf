resource "azurerm_cosmosdb_account" "db_account" {
  name                 = "${var.prefix}-exercise-12-cosmosdb-account"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  offer_type           = "Standard"
  kind                 = "MongoDB"
  mongo_server_version = 4.2

  capabilities {
    name = "EnableServerless"
  }

  capabilities { # forces replacement
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = "${var.prefix}-exercise-12-cosmosdb"
  resource_group_name = azurerm_cosmosdb_account.db_account.resource_group_name
  account_name        = azurerm_cosmosdb_account.db_account.name

  lifecycle {
    prevent_destroy = true
  }
}