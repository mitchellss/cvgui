"""FrameInput implementation for a computer webcam."""
from typing import Any
import numpy as np
import cv2


class Webcam:
    """FrameInput implementation for a computer webcam."""

    def __init__(self, device_num: int, fps: int) -> None:
        """Creates a new webcam frame input.

        Args:
            device_num (int): The device number of the webcam. Try 0 if unsure.
            fps (int): The frames per second the webcam can provide.
        """
        self.device_num = device_num
        self.fps = fps
        self.cap: cv2.VideoCapture = None

    def _configure(self) -> None:
        """
        Creates and configures the capture object. 

        This cannot be done in the init function because of how 
        Windows handles multiprocessing.
        """
        self.cap = cv2.VideoCapture(self.device_num)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FOURCC,
                     cv2.VideoWriter_fourcc("M", "J", "P", "G"))

    def get_frame(self) -> np.ndarray:
        """Gets a frame from the webcam."""
        if self.cap is None:
            self._configure()

        success: bool
        color_image: np.ndarray
        success, color_image = self.cap.read()
        if not success:
            return np.zeros(0)
        color_image = cv2.flip(color_image, 1)
        return color_image
