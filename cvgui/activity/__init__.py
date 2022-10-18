"""
Logic for running through an abstract activity.

The activity package is a handler that makes use of the
various interfaces described in the `core` package to
define how the components of the system should interact.
Since it only uses interfaces and does not reference
concrete implementations, the logic can be re-used for
any combination of concrete implementations that implement
those interfaces.
"""
from .activity import Activity  # noqa
from .scene import Scene  # noqa
