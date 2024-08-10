resource "azurerm_resource_group" "my-terraform-rg" {
  count = length(var.resource_groups)
  name     = var.resource_groups[count.index]
  location = "Germany West Central"
}
