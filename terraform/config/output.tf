output "Swarm Manager IPs" {
  value = "${digitalocean_droplet.managers.*.ipv4_address}"
}

output "Swarm Worker IPs" {
  value = "${digitalocean_droplet.workers.*.ipv4_address}"
}
