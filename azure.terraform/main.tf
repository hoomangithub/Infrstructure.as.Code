module "virtual_networks" {
  source = "./modules/vnet"
}

module "virtual_machine" {
  source = "./modules/vmlinux"
  resource_group_name = module.virtual_networks.resource_group_names
  resource_group_location = module.virtual_networks.resource_group_location
  network_interface_id = module.virtual_networks.network_interface_id
  security_group_id = module.virtual_networks.security_group_id
  depends_on = [
    module.virtual_networks
  ]
}