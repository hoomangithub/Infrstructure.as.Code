resource "random_string" "myrandom" {
  length  = 6
  upper   = false
  special = false
  numeric = false
}

resource "azurerm_public_ip" "mypublicip" {
  name                = "mypublicip-1"
  resource_group_name = azurerm_resource_group.my-terraform-rg[0].name
  location            = azurerm_resource_group.my-terraform-rg[0].location
  allocation_method   = "Static"
  sku                 = "Standard"
  domain_name_label   = "app1-vm-${random_string.myrandom.id}"
  tags = {
    environment = "DEV"
  }
  depends_on = [
    azurerm_resource_group.my-terraform-rg
  ]
}

resource "azurerm_network_interface" "myvmnic" {
  name                = "vmnic-1"
  location            = azurerm_resource_group.my-terraform-rg[0].location
  resource_group_name = azurerm_resource_group.my-terraform-rg[0].name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.mysubnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.mypublicip.id
    primary                       = true
  }

  tags = {
    environment = "DEV"
  }
  depends_on = [
    azurerm_resource_group.my-terraform-rg,
    azurerm_subnet.mysubnet,
    azurerm_public_ip.mypublicip
  ]
}