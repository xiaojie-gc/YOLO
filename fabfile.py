from fabric.api import env
env.use_ssh_config = True
env.password = 'Zxj_691012' 
from streamparse.ext.fabric import *


def pre_submit(topology_name, env_name, env_config, options):
    """Override this function to perform custom actions prior to topology
    submission. No SSH tunnels will be active when this function is called."""
    pass


def post_submit(topo_name, env_name, env_config, options):
    """Override this function to perform custom actions after topology
    submission. Note that the SSH tunnel to Nimbus will still be active
    when this function is called."""
    pass
