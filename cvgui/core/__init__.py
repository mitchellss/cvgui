"""
Interfaces that describe abstract component functionality.

The `core` package breaks down the program into its fundamental
functionality and defines an interface for each function. If
a concrete class is able to fulfill said interface, it can
therefore be considered fit to fulfill the requirements of
that function. For instance, both a MOCAP system and a
computer vision + camera combo can provide a set of points
when called upon that represent a human figure. These systems
therefore fulfill the requirements of the `recieving` core
package and could theoretically be implemented as core classes.
"""
from .displaying import (  # noqa
    UserInterface,
    skeleton,
    button,
    tracking_bubble,
    Skeleton,
    Button,
    TrackingBubble
  )
from .recieving import CVModel, FrameInput, PoseGenerator  # noqa
