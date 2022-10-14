"""Generates poses based on a computer vision model and a frame input."""
import numpy as np
from cvgui.core.recieving.service import CVModel, FrameInput


class ComputerVisionPose:
    """Generates poses based on a computer vision model and a frame input."""

    def __init__(self, frame_input: FrameInput, model: CVModel):
        """Creates a new pose generator based on a computer vision
        model.

        Args:
            frame_input (FrameInput): The input of images to the computer
            vision model.
            model (CVModel): The model use to interpret the images from
            the frame input.
        """
        self.frame_input: FrameInput = frame_input
        self.model: CVModel = model

    def get_pose(self) -> np.ndarray:
        """Uses the frame input and computer vision model in tandem
        to generate a single pose."""
        frame: np.ndarray = self.frame_input.get_frame()
        # Shaves about 5ms off each frame by passing by reference, not value
        frame.flags.writeable = False
        pose: np.ndarray = self.model.get_pose(frame)
        return pose
