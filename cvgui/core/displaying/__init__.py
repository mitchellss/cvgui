"""
Package for graphically displaying data to the user.

The `displaying` core package provides interfaces
that describe what methods a user interface must implement
to be able to display data to a user correctly.
"""

from .service import UserInterface
from .components import skeleton, button, Skeleton, Button
