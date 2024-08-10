resource "azurerm_resource_group" "my-terraform-rg" {
  count = length(var.resource_groups)
  name     = var.resource_groups[count.index]
  location = "Germany West Central"
}

# Alternative to count
# locals {
#   resource_groups_list = [
#     "my-rg-1",
#     "my-rg-2"
#   ]
# }
# resource "azurerm_resource_group" "my-terraform-rg-2" {
#   for_each = toset(local.resource_groups_list)
#   name     = each.value
#   location = "Germany West Central"
# }
