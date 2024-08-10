output "resource_group_names" {
  value = [for rg in azurerm_resource_group.my-terraform-rg : rg.name]
}

output "azurerm_subnet_name" {
  value = azurerm_subnet.mysubnet.name
}