data "template_file" "inventory" {
  template = "${file("templates/inventory.tpl")}"

  depends_on = [
    "digitalocean_droplet.managers",
    "digitalocean_droplet.workers",
  ]

  vars {
    managers = "${join("\n", "${digitalocean_droplet.managers.*.ipv4_address}")}"
    workers  = "${join("\n", "${digitalocean_droplet.workers.*.ipv4_address}")}"
  }
}

data "template_file" "blog_state" {
  template = "${file("templates/blog-state.json.tpl")}"

  depends_on = [
    "digitalocean_droplet.managers",
    "digitalocean_droplet.workers",
  ]

  vars {
    managers = "${join(",", formatlist("\"%s\"", digitalocean_droplet.managers.*.ipv4_address))}"
    workers  = "${join(",", formatlist("\"%s\"", digitalocean_droplet.workers.*.ipv4_address))}"
  }
}

resource "null_resource" "cmd" {
  triggers {
    template_rendered = "${data.template_file.inventory.rendered}"
  }
  
  provisioner "local-exec" {
    command = "echo '${data.template_file.inventory.rendered}' > ${var.ansible_dir}/inventory.ini"
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.blog_state.rendered}' > ${var.instance_state_file}"
  }

  provisioner "local-exec" {
    when    = "destroy"
    command = "echo '' > ../ansible/inventory.ini && echo '{}' > ${var.instance_state_file}"
  }

  provisioner "local-exec" {
    command = <<EOT
      cd ${var.ansible_dir} && \
      ansible-playbook -i inventory.ini --private-key ${var.ssh_private_key} setup.playbook.yml
    EOT
  }
}
