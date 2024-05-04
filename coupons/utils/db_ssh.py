# Configuración del túnel SSH
from sshtunnel import SSHTunnelForwarder
import dotenv
import os

dotenv.load_dotenv()

SSH_HOST = os.environ.get('SSH_HOT')
SSH_PORT = int(os.environ.get('SSH_PORT'))
SSH_USERNAME = os.environ.get('SSH_USERNAME')
SSH_PASSWORD = os.environ.get('SSH_PASSWORD')

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