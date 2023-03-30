"""CVModel implementation for Google's Blazepose."""
import logging
import numpy as np
import mediapipe as mp


class BlazePose:
    """CVModel implementation for Google's Blazepose."""

    LEFT_HAND: int = 16
    """Blazepose left hand"""
    LEFT_ELBOW: int = 14
    """Blazepose left elbow"""
    LEFT_SHOULDER: int = 12
    """Blazepose left shoulder"""
    LEFT_HIP: int = 24
    """Blazepose left hip"""
    LEFT_KNEE: int = 26
    """Blazepose left knee"""
    LEFT_FOOT: int = 28
    """Blazepose left foot"""
    RIGHT_HAND: int = 17
    """Blazepose right hand"""
    RIGHT_ELBOW: int = 13
    """Blazepose right elbow"""
    RIGHT_SHOULDER: int = 11
    """Blazepose right shoulder"""
    RIGHT_HIP: int = 23
    """Blazepose right hip"""
    RIGHT_KNEE: int = 25
    """Blazepose right knee"""
    RIGHT_FOOT: int = 27
    """Blazepose right foot"""

    DEFAULT_SCALE: int = 450

    def __init__(self, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5,
                 model_complexity: int = 1) -> None:
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.model_complexity = model_complexity
        self.pose_array = np.zeros((33, 4))  # TODO: make these constants
        self.model = None

    def _configure(self):
        """
        Creates the blazepose model.

        This cannot be done in the init function due to how Windows handles
        multiprocessing.
        """
        mp_pose = mp.solutions.pose  # type: ignore
        self.model = mp_pose.Pose(
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
            model_complexity=self.model_complexity)

    def get_pose(self, frame: np.ndarray) -> np.ndarray:
        """Processes an image using Google's BlazePose and
        returns the pose data (skeleton)."""
        if self.model is None:
            self._configure()

        try:
            landmarks = self.model.process(frame)
            pose = landmarks.pose_world_landmarks.landmark
            for landmark, _ in enumerate(pose):
                # Save raw data for logging purposes
                self.pose_array[landmark][0] = pose[landmark].x
                self.pose_array[landmark][1] = pose[landmark].y
                self.pose_array[landmark][2] = pose[landmark].z
                self.pose_array[landmark][3] = pose[landmark].visibility
            return self.pose_array
        except AttributeError:
            # This error is thrown when a pose
            # is not found in the image provided
            return self.pose_array
        except KeyboardInterrupt as excpt:
            logging.info("Ctrl-C pressed...")
            raise excpt
