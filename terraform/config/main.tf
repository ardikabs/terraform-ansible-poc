provider "digitalocean" {
  token = "${var.do_token}"
}

resource "digitalocean_ssh_key" "ssh" {
  name       = "Blog"
  public_key = "${file("${var.ssh_dir}/id_rsa.pub")}"
}

resource "digitalocean_droplet" "managers" {
  depends_on = [
    "digitalocean_ssh_key.ssh",
  ]

  count    = "${var.swarm_managers}"
  name     = "${upper("pr-blog-manager-${count.index + 1}")}"
  image    = "ubuntu-16-04-x64"
  region   = "sgp1"
  size     = "s-1vcpu-2gb"
  ssh_keys = ["${digitalocean_ssh_key.ssh.fingerprint}"]
}

resource "digitalocean_droplet" "workers" {
  depends_on = [
    "digitalocean_droplet.managers",
  ]

  count    = "${var.swarm_workers}"
  name     = "${upper("pr-blog-worker-${count.index + 1}")}"
  image    = "ubuntu-16-04-x64"
  region   = "sgp1"
  size     = "s-1vcpu-1gb"
  ssh_keys = ["${digitalocean_ssh_key.ssh.fingerprint}"]
}
