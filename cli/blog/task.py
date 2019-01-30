
from fabric import Connection

def get_connection(host, user, keyfile):
    return Connection(host, user, connect_kwargs={"key_filename": keyfile})

def transfer():
    pass

def deploy(conn):
    conn.run("git clone https://github.com/ardikabs/blog-automation-docker-compose.git")
    conn.run("sleep 3")
    conn.run("docker stack deploy -c blog-automation-docker-compose/docker-compose.yml blog")

def check_server_count(conn):
    conn.run("docker service inspect -f \"{{ .Spec.Mode.Replicated.Replicas }}\" blog_wordpress")

def scaler(conn, count):
    conn.run(f"docker service scale blog_wordpress={count}")