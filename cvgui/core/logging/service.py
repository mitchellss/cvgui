"""The service module contains interfaces related to \
    logging."""
import multiprocessing.queues as mpq
import multiprocessing as mp
from typing import Iterable, Protocol


class PoseLogger(Protocol):
    """Defines the behavior of an object \
        that logs the user's pose over \
            time."""

    def start(
            self, pose_queue: mpq.Queue
    ) -> Iterable[mp.Process]:  # type: ignore
        """Initialize the pose logger. This is done here \
            instead of the init function due to the way \
                windows handles multiprocessing."""

    def log_data(self, pose_queue: mpq.Queue) -> None:
        """Log data from the queue."""

    def save(self) -> bool:  # type: ignore
        """Save logged data to the disk."""

    def close(self) -> bool:  # type: ignore
        """Finish logging poses and safely close any \
        files or repositories."""
