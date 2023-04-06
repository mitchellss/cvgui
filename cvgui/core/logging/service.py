import multiprocessing as mp
from typing import Iterable, Protocol


class PoseLogger(Protocol):

    def start(
            self, pose_queue: mp.Queue
    ) -> Iterable[mp.Process]:  # type: ignore
        """
        Initializes the pose logger.
        """

    def log_data(self, pose_queue: mp.Queue) -> None:
        """
        Log data from the queue.
        """

    def save(self) -> bool:  # type: ignore
        """
        Save logged data to the disk.
        """

    def close(self) -> bool:  # type: ignore
        """
        Finish logging poses and safely close any
        files or repositories.
        """
