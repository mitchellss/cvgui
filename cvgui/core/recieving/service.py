"""Interfaces describing methods of recieving data."""
from typing import Iterable
from typing_extensions import Protocol
import numpy as np


class CVModel(Protocol):
    """The requirements to be considered a computer vision model."""

    LEFT_HAND: int
    """Index of the model's pose array that
    represents the user's left hand"""

    LEFT_ELBOW: int
    """Index of the model's pose array that
    represents the user's left elbow"""

    LEFT_SHOULDER: int
    """Index of the model's pose array that
    represents the user's left shoulder"""

    LEFT_HIP: int
    """Index of the model's pose array that
    represents the user's left hip"""

    LEFT_KNEE: int
    """Index of the model's pose array that
    represents the user's left knee"""

    LEFT_FOOT: int
    """Index of the model's pose array that
    represents the user's left foot"""

    RIGHT_HAND: int
    """Index of the model's pose array that
    represents the user's right hand"""

    RIGHT_ELBOW: int
    """Index of the model's pose array that
    represents the user's right elbow"""

    RIGHT_SHOULDER: int
    """Index of the model's pose array that
    represents the user's right shoulder"""

    RIGHT_HIP: int
    """Index of the model's pose array that
    represents the user's right hip"""

    RIGHT_KNEE: int
    """Index of the model's pose array that
    represents the user's right knee"""

    RIGHT_FOOT: int
    """Index of the model's pose array that
    represents the user's right foot"""

    DEFAULT_SCALE: int
    """How the model should be sized by default"""

    def get_pose(self, frame: np.ndarray) -> np.ndarray:  # type: ignore
        """Retrieves the points making up a pose (skeleton) for a given
        image.

        Args:
            frame (np.ndarray): An image. Generally one image in a
            sequence of images that make up a video.

        Returns:
            np.ndarray: An array of points that describe the
            locations of various points of a pose (skeleton).
        """


class FrameInput(Protocol):
    """
    Abstract object that can provide image frames on-demand
    such as a webcam input or video file.
    """

    def get_frame(self) -> np.ndarray:  # type: ignore
        """Retrieve a frame from the repository.

        Returns:
            np.ndarray: An array of points that describe the
            locations of points of a pose (skeleton).
        """


class PoseGenerator(Protocol):
    """
    Abstract generator of poses (skeletons) such as a computer
    vision model or a motion capture system.
    """

    def get_pose(self) -> np.ndarray:  # type: ignore
        """Retrieve a pose from the generator.

        Returns:
            np.ndarray: An array of points that describe the
            locations of points of a pose (skeleton).
        """

    def start(self, skeleton_queue) -> Iterable:  # type: ignore
        """
        Completes any configuration that needs to be done
        after initialization. Useful if the frame input is
        being run in a separate process so that configruation
        can be done post-fork.
        """
