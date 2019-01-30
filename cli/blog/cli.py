import click
import configparser
import json

from . import __version__
from .commands import *
from .config import ConfigFileProcessor

@click.group(invoke_without_command=True)
@click.version_option(
    version=__version__, 
    prog_name="Blog",
    message=('%(prog)s version %(version)s')
)
@click.option("--config-path", 
    type=click.Path(exists=True),
    envvar="BLOG_CONFIG_PATH", 
    help="Configuration file path. You can set with ENV variable (BLOG_CONFIG_PATH) to be loaded automatically"
)
@click.pass_context
def cli(ctx, config_path):
    cfp = ConfigFileProcessor()
    if config_path:
        cfp.config_searchpath = [config_path]
    try:
        config = cfp.read_config()
    except configparser.DuplicateOptionError as e:
        click.echo(f"Error: Config ({e.source}). " 
                    f"Option <{e.option}> in section ({e.section}) "
                    f"already exist [line {e.lineno}]"
        )
        ctx.exit(0)
    except configparser.DuplicateSectionError as e:
        click.echo(f"Error: Config ({e.source}). " 
                    f"Duplicate section ({e.section}) [line {e.lineno}]"
        )
        ctx.exit(0)
    
    if not config:
        raise click.ClickException(
            message="No configuration file found [cerberus.cfg / cerberus.ini]"
        )
    ctx.ensure_object(dict)
    ctx.obj["CONFIG"] = config
    ctx.obj["CONFIG_PATH"] = cfp.config_path
    ctx.obj["DIGITAL_OCEAN_TOKEN"] = config["cloud"]["token"]
    ctx.obj["SSH_DIRECTORY"] = config["ssh"]["ssh_dir"][:-1] \
                                if config["ssh"]["ssh_dir"].endswith("/") else config["ssh"]["ssh_dir"]
    ctx.obj["INITIAL_SWARM_CLUSTER_MANAGERS"] = config["swarm_cluster"]["managers"]
    ctx.obj["INITIAL_SWARM_CLUSTER_WORKERS"] = config["swarm_cluster"]["workers"]

    state_file = config["state"]
    ctx.obj["STATE"] = json.load(open(state_file, "r"))
    ctx.obj["STATE_FILE"] = state_file

cli.add_command(setup)
cli.add_command(up)
cli.add_command(down)
cli.add_command(scale)
cli.add_command(status)

