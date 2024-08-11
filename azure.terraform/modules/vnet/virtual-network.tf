resource "azurerm_virtual_network" "myvnet" {
  name                = "myvnet-1"
  address_space       = ["10.0.0.0/25"]
  location            = azurerm_resource_group.my-terraform-rg[0].location
  resource_group_name = azurerm_resource_group.my-terraform-rg[0].name
  tags = {
    "environment" = "DEV"
  }
  depends_on = [
    azurerm_resource_group.my-terraform-rg
  ]
}

resource "azurerm_subnet" "mysubnet" {
  name                 = "mysubnet-1"
  resource_group_name  = azurerm_resource_group.my-terraform-rg[0].name
  virtual_network_name = azurerm_virtual_network.myvnet.name
  address_prefixes = ["10.0.0.0/26"]
  depends_on = [
    azurerm_virtual_network.myvnet
  ]
}
