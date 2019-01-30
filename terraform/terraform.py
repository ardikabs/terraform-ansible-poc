# !/usr/bin/python3

import click
import os
import subprocess
import datetime

workdir = os.path.dirname(os.path.abspath(__file__))

@click.group()
def cli():
    pass


@cli.command("provision", help="Provisioning instances")
@click.option("--do-token", "do_token", help="DigitalOcean API Token")
@click.option("--swarm-managers", help="Swarm Manager Initial Count")
@click.option("--swarm-workers", help="Swarm Worker Initial Count")
@click.option("--ssh-dir", help="SSH config directory")
@click.option("--ansible-dir", help="Ansible directory")
@click.option("--instance-state-file", help="Instance state file path")
def provisioning(do_token, swarm_managers, swarm_workers, ssh_dir, ansible_dir, instance_state_file):
    now = datetime.datetime.today().strftime('%d%M%y%H%M')
    plan_format = f"{now}.plan"

    commands = f"terraform init && " \
            f"terraform validate config/ && " \
            f"terraform plan -var 'do_token={do_token}' -var 'ssh_dir={ssh_dir}' " \
            f"-var 'swarm_managers={swarm_managers}' -var 'swarm_workers={swarm_workers}' " \
            f"-var 'ansible_dir={ansible_dir}' -var 'instance_state_file={instance_state_file}' " \
            f"-state=state/terraform.tfstate -out=plan/{plan_format} config/ && " \
            f"terraform apply -auto-approve "\
            f"-state-out=state/terraform.tfstate -input=false plan/{plan_format}"
    
    process = subprocess.run(commands, shell=True)

@cli.command("destroy", help="Destroying instances")
@click.option("--do-token", "do_token", help="DigitalOcean API Token")
@click.option("--ssh-dir", help="SSH config directory")
@click.option("--ansible-dir", help="Ansible directory")
@click.option("--instance-state-file", help="Instance state file path")
def destroying(do_token, ssh_dir, ansible_dir, instance_state_file):
    now = datetime.datetime.today().strftime('%d%M%y%H%M')
    destroy_plan_format = f"{now}.destroy"

    commands = f"terraform plan -destroy -state=state/terraform.tfstate " \
        f"-var 'ansible_dir={ansible_dir}' -var 'instance_state_file={instance_state_file}' " \
        f"-var 'do_token={do_token}' -var 'ssh_dir={ssh_dir}' -out=plan/{destroy_plan_format} config/ && " \
        f"terraform apply -auto-approve "\
        f"-state-out=state/terraform.tfstate "\
        f"-input=false plan/{destroy_plan_format}"
    
    process = subprocess.run(commands, shell=True)

if __name__ == "__main__":
    cli()