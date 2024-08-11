locals {
  app_inbound_ports_map = {
    "100" : "80",
    "110" : "443",
    "120" : "8080"
  }
}

resource "azurerm_network_security_group" "app_subnet_nsg" {
  name                = "${azurerm_subnet.mysubnet.name}-ng"
  location            = azurerm_resource_group.my-terraform-rg[0].location
  resource_group_name = azurerm_resource_group.my-terraform-rg[0].name
  depends_on = [
    azurerm_resource_group.my-terraform-rg,
    azurerm_subnet.mysubnet
  ]
}

resource "azurerm_network_security_rule" "app_nsg_rule_inbound" {
  for_each                    = local.app_inbound_ports_map
  name                        = "Rule-Port-${each.value}"
  priority                    = each.key
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = each.value
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.my-terraform-rg[0].name
  network_security_group_name = azurerm_network_security_group.app_subnet_nsg.name
  depends_on = [
    azurerm_resource_group.my-terraform-rg,
    azurerm_network_security_group.app_subnet_nsg
  ]
}

resource "azurerm_network_security_rule" "app_nsg_rule_inbound_port_22" {
  name                        = "Rule-Port-22"
  priority                    = "130"
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "87.78.113.98"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.my-terraform-rg[0].name
  network_security_group_name = azurerm_network_security_group.app_subnet_nsg.name
  depends_on = [
    azurerm_resource_group.my-terraform-rg,
    azurerm_network_security_group.app_subnet_nsg,
    azurerm_network_security_rule.app_nsg_rule_inbound
  ]
}

resource "azurerm_subnet_network_security_group_association" "app_subnet_nsg_associate" {
  subnet_id                 = azurerm_subnet.mysubnet.id
  network_security_group_id = azurerm_network_security_group.app_subnet_nsg.id
  depends_on = [
    azurerm_network_security_group.app_subnet_nsg,
    azurerm_subnet.mysubnet
  ]
}