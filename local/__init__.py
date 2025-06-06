"""
Local testing modules for fast_sync_udp.

This package contains modules for running the entire lab setup locally on a single PC.
"""

# Local testing configuration
from . import local_config

# Local communication classes (simplified, no sudo required)
from . import local_comms
from . import local_utils
from . import local_db

# Local testing applications
from . import local_server
from . import local_client
from . import run_local_test 