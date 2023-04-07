"""
.. include:: ../README.md
"""

# These two need to be at the top to silence the pygame
# welcome message in the terminal.
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from .outputs import *  # noqa
from .core import *  # noqa
from .inputs.computer_vision import *  # noqa
from .user_interface import *  # noqa
from .activity import *  # noqa
