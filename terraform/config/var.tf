variable "ssh_private_key" {
  default = "~/.ssh/id_rsa"
}
variable "ssh_public_key" {
  default = "~/.ssh/id_rsa.pub"
}

variable "ansible_dir" {
  default = "../ansible"
}

variable "instance_state_file" {
  default = "blog-state.json"
}

variable "do_token" {
  default = ""
}

variable "swarm_managers" {
  default = 1
}

variable "swarm_workers" {
  default = 1
}
