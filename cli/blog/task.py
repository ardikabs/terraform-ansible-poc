
from fabric import Connection

def get_connection(host, user, keyfile):
    return Connection(host, user, connect_kwargs={"key_filename": keyfile})

def deploy(conn, debug=True):
    hide = False if debug else True
    return conn.run(
        "git clone https://github.com/ardikabs/blog-automation-docker-compose.git && " \
        "sleep 3 && " \
        "docker stack deploy -c blog-automation-docker-compose/docker-compose.yml blog", hide=hide
    )

def check_server_count(conn):
    return conn.run("docker service inspect -f \"{{ .Spec.Mode.Replicated.Replicas }}\" blog_wordpress", hide=True)

def scaler(conn, count, debug=True):
    hide = False if debug else True
    return conn.run(f"docker service scale blog_wordpress={count}", hide=hide)