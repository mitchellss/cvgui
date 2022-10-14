"""The requirements to be considered a computer vision model."""
from typing_extensions import Protocol
import numpy as np


class CVModel(Protocol):
    """Interface describing a computer vision model's methods."""
    LEFT_HAND: int
    LEFT_ELBOW: int
    LEFT_SHOULDER: int
    LEFT_HIP: int
    LEFT_KNEE: int
    LEFT_FOOT: int
    RIGHT_HAND: int
    RIGHT_ELBOW: int
    RIGHT_SHOULDER: int
    RIGHT_HIP: int
    RIGHT_KNEE: int
    RIGHT_FOOT: int

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
    """Abstract repository that can provide image frames such as a
    webcam input or video file."""

    def get_frame(self) -> np.ndarray:  # type: ignore
        """Retrieve a frame from the repository."""


class PoseGenerator(Protocol):
    """Abstract generator of poses (skeletons) such as a computer
    vision model or a motion capture system."""

    def get_pose(self) -> np.ndarray:  # type: ignore
        """Retrieve a pose from the generator."""
