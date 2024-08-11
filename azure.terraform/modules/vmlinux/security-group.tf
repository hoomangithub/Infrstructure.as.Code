resource "azurerm_network_interface_security_group_association" "web_linuxvm_nsg_associate" {
  network_interface_id = var.network_interface_id
  network_security_group_id = var.security_group_id
}

