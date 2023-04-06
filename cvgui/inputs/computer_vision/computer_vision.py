"""
The computer_vision module contains the main ComputerVisionPose class \
    that dictates the interactions between frame inputs and computer \
        vision models.
"""
from typing import Any, Iterable
import cv2
import numpy as np
import multiprocessing as mp
from cvgui.core.receiving.service import CVModel, FrameInput


class ComputerVisionPose:
    """Generates poses based on a computer vision model and a frame input."""

    def __init__(self, frame_input: FrameInput, model: CVModel) -> None:
        """Creates a new pose generator based on a computer vision \
        model.

        Args:
            frame_input (FrameInput): The input of images \
            to the computer vision model.
            model (CVModel): The model use to interpret the images \
            from the frame input.
        """
        self.frame_input: FrameInput = frame_input
        self.model: CVModel = model

    def start(self, pose_queue: mp.Queue) -> Iterable[mp.Process]:
        """
        Starts two processes, one for \
        capturing/displaying frame input data and \
        one for processing that frame input \
        data to get poses out of them. \
        These are done as separate processes \
        because otherwise the pose \
        processing greatly slows down the \
        speed at which frames are collected, \
        resulting in video feedback that is "laggy". \

        Args:
            pose_queue (multiprocessing.Queue): The queue to put pose \
                data into once it has been processed from frames.

        Returns:
            list[multiprocessing.Process]: All the processes started by this \
                method so they can be closed correctly later down the line.
        """
        image_queue: mp.Queue = mp.Queue()
        print("Starting image processing pipeline "
              "(This might take a while on Windows)...")
        cap = mp.Process(target=self._capture_and_show, args=(image_queue,))
        proc = mp.Process(target=self._process_image,
                          args=(image_queue, pose_queue))
        cap.start()
        proc.start()
        return [cap, proc]

    def _capture_and_show(self, image_queue) -> None:
        """
        Infinitely retrieves new frames and places them in the image \
        queue. Additionally, displays incoming frames to the user in \
        real-time.
        """
        while True:
            frame: np.ndarray = self.frame_input.get_frame()
            image_queue.put(frame)
            cv2.imshow("Video Input", frame)
            wait_key: Any = cv2.waitKey(1)
            if wait_key == 27:
                pass

    def _process_image(self, image_queue, pose_queue) -> None:
        """
        Infinitely takes images from the given queue and turns them into \
        pose data using a computer vision model.
        """
        while True:
            if image_queue.empty():
                continue
            pose: np.ndarray = self.model.get_pose(image_queue.get())
            pose_queue.put(pose)

    def get_pose(self) -> np.ndarray:
        """
        Uses the frame input and computer vision model in tandem \
        to generate a single pose.
        """
        frame: np.ndarray = self.frame_input.get_frame()
        # Shaves about 5ms off each frame by passing by reference, not value
        frame.flags.writeable = False
        pose: np.ndarray = self.model.get_pose(frame)
        return pose
