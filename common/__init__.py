"""
Common modules for IEEE C37.118.2 synchrophasor implementation.

This package contains shared modules used by both local testing and lab deployment.
"""

# Core IEEE C37.118.2 implementation
from . import frame

# Communication classes
from . import cl_inherited_comms
from . import cl_utils

# Utilities
from . import utils 