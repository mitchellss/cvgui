"""FrameInput implementation for a computer webcam."""
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
        self.cap = cv2.VideoCapture(device_num)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_FOURCC,
                     cv2.VideoWriter_fourcc("M", "J", "P", "G"))

    def get_frame(self) -> np.ndarray:
        """Gets a frame from the webcam."""
        success: bool
        color_image: np.ndarray
        success, color_image = self.cap.read()
        if not success:
            return np.zeros(0)
        color_image = cv2.flip(color_image, 1)

        cv2.imshow("Video Playback", color_image)
        wait_key = cv2.waitKey(1)
        if wait_key == 27:
            pass
        return color_image
