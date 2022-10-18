"""
Package for recieving human pose data.

The `recieving` core package provides interfaces
that describe how human pose data should be recieved
by the system. Pose data can either be retrieved by
a combination of a computer vision model and frame input
or through a generic pose generator.
"""
from .service import CVModel, FrameInput, PoseGenerator  # noqa
