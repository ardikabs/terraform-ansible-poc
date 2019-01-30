
import time
import os
import json
import click
import subprocess

from .task import *

workdir = os.path.dirname(os.path.abspath(__name__))

@click.command("setup", help="Setup blog instances (managers & workers)")
@click.option("-d", "--debug", is_flag=True, help="Debugging optional")
@click.pass_context
def setup(ctx, debug):
    print(f"Setup Blog Instances")
    print(f"Please wait ...")

    do_token = ctx.obj["DIGITAL_OCEAN_TOKEN"]
    ssh_dir = ctx.obj["SSH_DIRECTORY"]
    state_file = ctx.obj["STATE_FILE"]
    swarm_managers = ctx.obj.get("INITIAL_SWARM_CLUSTER_MANAGERS", 1)
    swarm_workers = ctx.obj.get("INITIAL_SWARM_CLUSTER_WORKERS", 1)

    terraform_dir = f"{workdir}/terraform"
    ansible_dir = f"{workdir}/ansible"
    
   
    stdout = subprocess.PIPE
    if debug:
        stdout = None
    try:
        commands = f"cd {terraform_dir} && " \
            f"python terraform.py provision --do-token {do_token} --ssh-dir {ssh_dir} " \
            f"--ansible-dir {ansible_dir} --instance-state-file {state_file} " \
            f"--swarm-managers {swarm_managers} --swarm-workers {swarm_workers}"

        terraform = subprocess.run(
            commands,
            stdout=stdout,
            shell=True,
            check=True
        )

        time.sleep(10)
        
        commands = f"cd {ansible_dir} && " \
            f"ansible-playbook -i inventory.ini setup.playbook.yml" 

        ansible = subprocess.run(
            commands,
            stdout=stdout,
            shell=True,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        click.echo(f"Error: {exc.returncode}")
    else:
        jsonfile = open("blog-state.json", "r")
        state = json.load(jsonfile)
        click.echo("\n=====================================================")
        click.echo(f"Swarm manager already setup ({state['managers'][0]})")
        click.echo(f"Swarm ready to be deployed a service")

@click.command("up", help="Start service on blog instances")
@click.option("-d", "--debug", is_flag=True, help="Debugging optional")
@click.pass_context
def up(ctx, debug):
    ssh_dir = ctx.obj["SSH_DIRECTORY"]
    state = ctx.obj["STATE"]

    if not state:
        click.echo("Error: You need to setup the instance before starting the service")
        ctx.exit(1)
    
    conn = get_connection(state["managers"][0], "root", f"{ssh_dir}/id_rsa")
    deploy(conn)
    click.echo(f"Blog can be access in http://{state['managers'][0]}:8000")

@click.command("down", help="Stop service and blog instances")
@click.option("-d", "--debug", is_flag=True, help="Debugging optional")
@click.pass_context
def down(ctx, debug):
    click.echo(f"Shutdown Blog Instances")
    click.echo(f"Please wait ...")

    do_token = ctx.obj["DIGITAL_OCEAN_TOKEN"]
    ssh_dir = ctx.obj["SSH_DIRECTORY"]
    state_file = ctx.obj["STATE_FILE"]

    terraform_dir = f"{workdir}/terraform"
    ansible_dir = f"{workdir}/ansible"

    commands = f"cd {terraform_dir} && " \
        f"python terraform.py destroy --do-token {do_token} --ssh-dir {ssh_dir} " \
        f"--ansible-dir {ansible_dir} --instance-state-file {state_file}"
    
    stdout = subprocess.PIPE
    if debug:
        stdout = None
    try:
        terraform = subprocess.run(
            commands,
            stdout=stdout,
            shell=True,
            check=True
        )

        time.sleep(3)
    except subprocess.CalledProcessError as exc:
        click.echo(f"Error: {exc.returncode}")
    else:
        click.echo(f"All Blog instances already shutdown")

@click.command("scale", help="Scale one or multiple blog instances (only blog)")
@click.argument("NUMBER_OF_SERVICE", type=click.INT)
@click.option("-d", "--debug", is_flag=True, help="Debugging optional")
@click.pass_context
def scale(ctx, debug, number_of_service):
    ssh_dir = ctx.obj["SSH_DIRECTORY"]
    state = ctx.obj["STATE"]
    if not state:
        click.echo("Error: You need to setup the instance before starting the service")
        ctx.exit(1)
    conn = get_connection(state["managers"][0], "root", f"{ssh_dir}/id_rsa")
    scaler(conn, number_of_service)

@click.command("status", help="Check number of server instance")
@click.option("-d", "--debug", is_flag=True, help="Debugging optional")
@click.pass_context
def status(ctx, debug):
    ssh_dir = ctx.obj["SSH_DIRECTORY"]
    state = ctx.obj["STATE"]

    if not state:
        click.echo("Error: You need to setup the instance before starting the service")
        ctx.exit(1)
    
    conn = get_connection(state["managers"][0], "root", f"{ssh_dir}/id_rsa")
    check_server_count(conn)