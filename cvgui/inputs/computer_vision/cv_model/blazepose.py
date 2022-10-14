"""CVModel implementation for Google's Blazepose."""
import logging
import numpy as np
import mediapipe as mp


class BlazePose:
    """CVModel implementation for Google's Blazepose."""
    LEFT_HAND: int = 16
    LEFT_ELBOW: int
    LEFT_SHOULDER: int
    LEFT_HIP: int
    LEFT_KNEE: int
    LEFT_FOOT: int
    RIGHT_HAND: int = 17
    RIGHT_ELBOW: int
    RIGHT_SHOULDER: int
    RIGHT_HIP: int
    RIGHT_KNEE: int
    RIGHT_FOOT: int

    def __init__(self) -> None:
        self.pose_array = np.zeros((33, 4))
        self.mp_pose = mp.solutions.pose  # type: ignore
        self.model = self.mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=1)

    def get_pose(self, frame: np.ndarray) -> np.ndarray:
        """Processes an image using Google's BlazePose and
        returns the pose data (skeleton)."""
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
            # This error is thrown when a pose is not found in the image provided
            return self.pose_array
        except KeyboardInterrupt as excpt:
            logging.info("Ctrl-C pressed...")
            raise excpt
