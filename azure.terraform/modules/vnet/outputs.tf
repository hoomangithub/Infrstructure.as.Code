output "resource_group_names" {
  value = [for rg in azurerm_resource_group.my-terraform-rg : rg.name]
}

output "resource_group_location" {
  value =  [for rg in azurerm_resource_group.my-terraform-rg : rg.location]
}

output "virtual_network_name" {
  value = azurerm_virtual_network.myvnet.name
}

output "virtual_network_id" {
  value = azurerm_virtual_network.myvnet.id
}

output "subnet_name" {
  value = azurerm_subnet.mysubnet.name
}

output "subnet_id" {
  value = azurerm_subnet.mysubnet.id
}

output "app_subnet_nsg_nme" {
  value = azurerm_network_security_group.app_subnet_nsg.name
}

output "app_subnet_nsg_id" {
  value = azurerm_network_security_group.app_subnet_nsg.id
}

output "network_interface_id" {
  value = azurerm_network_interface.myvmnic.id
}

output "security_group_id" {
  value = azurerm_network_security_group.app_subnet_nsg.id
}