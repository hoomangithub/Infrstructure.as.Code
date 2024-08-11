output "resource_group_names" {
  value = module.virtual_networks.resource_group_names
}

output "virtual_network_name" {
  value = module.virtual_networks.virtual_network_name
}

output "subnet_nsg_nme" {
  value = module.virtual_networks.app_subnet_nsg_nme
}

output "resource_group_location" {
  value = module.virtual_networks.resource_group_location
}

output "security_group_id" {
  value = module.virtual_networks.security_group_id
}

output "web_linuxvm_public_ip_address" {
  value = module.virtual_machine.web_linuxvm_public_ip_address
}

output "web_linuxvm_private_ip_address" {
  value = module.virtual_machine.web_linuxvm_private_ip_address
}

