"""
Package for graphically displaying data to the user.

The `displaying` core package provides interfaces
that describe what methods a user interface must implement
to be able to display data to a user correctly.
"""

from .service import UserInterface  # noqa
from .components import (  # noqa
    skeleton,
    button,
    tracking_bubble,
    Skeleton,
    Button,
    TrackingBubble
)
