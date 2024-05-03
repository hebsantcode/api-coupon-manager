# Configuración del túnel SSH
from sshtunnel import SSHTunnelForwarder

SSH_HOST = 'premium166.web-hosting.com'
SSH_PORT = 21098
SSH_USERNAME = 'creafzdi'
SSH_PASSWORD = 'sAntiago110812'

def setup_ssh_tunnel():
    # Set up ssh tunnel
    tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=('127.0.0.1', 5432),  
        local_bind_address=('127.0.0.1', 5437), # Puerto del túnel SSH
    )
    tunnel.start()
    print(tunnel.tunnel_is_up) # Tell if the tunnel is listening