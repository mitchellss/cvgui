"""
The `computer_vision` package implements the interfaces described \
    in the `cvgui.core.receiving` package. These interfaces \
        allow `computer_vision` to be used as a pose generator \
            in user-created activites.
"""
from .cv_model.blazepose import BlazePose  # noqa
from .frame_input.webcam import Webcam  # noqa
from .computer_vision import ComputerVisionPose  # noqa
