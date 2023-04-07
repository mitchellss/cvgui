"""Collection of interfaces for receiving data."""
from typing import Iterable
import multiprocessing as mp
import multiprocessing.queues as mpq
from typing_extensions import Protocol
import numpy as np


class CVModel(Protocol):
    """Abstract object that can generate a pose given \
        an consisting of various body parts."""

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
        """Retrieve the pose for a given image.

        Args:
            frame (np.ndarray): A numpy array representing an image.

        Returns:
            np.ndarray: An array of points that describe the pose.
        """


class FrameInput(Protocol):
    """Abstract object that can provide image \
        frames on-demand such as a webcam input \
            or video file."""

    def get_frame(self) -> np.ndarray:  # type: ignore
        """Retrieve a frame from the repository.

        Returns:
            np.ndarray: An array of points that describe the
            locations of points of a pose (skeleton).
        """


class PoseGenerator(Protocol):
    """Abstract generator of poses such as a computer \
    vision model or a motion capture system."""

    def get_pose(self) -> np.ndarray:  # type: ignore
        """Retrieve a pose from the generator.

        Returns:
            np.ndarray: An array of points that describe the \
            locations of points of a pose.
        """

    def start(self,
              pose_queues: Iterable[mpq.Queue]
              ) -> Iterable[mp.Process]:  # type: ignore
        """
        Completes any configuration that needs to be done \
        after initialization. Useful if the frame input is \
        being run in a separate process so that configruation \
        can be done post-fork.

        Args:
            pose_queue (mpq.Queue): The multiprocessing queue to put \
                pose data in.

        Returns:
            Iterable[mp.Process]: A collection of processes started \
                by the function that must be cleaned up later.
        """
