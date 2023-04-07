"""The `csv_logger` module contains \
classes related to logging data to csv \
files."""
from pathlib import Path
import time
from typing import Iterable, List
import multiprocessing as mp
import multiprocessing.queues as mpq
import numpy as np


class CSVPoseLogger:
    """A pose logger that saves data to a csv file."""

    active: bool = True
    """Whether the logger should be actively saving \
        pose data."""

    def __init__(self, filepath: Path) -> None:
        """Create a new csv logger.

        Args:
            filepath (Path): The path to where the csv log \
                file should be saved.
        """
        self.filepath: Path = filepath
        self.data: np.ndarray = None
        self.size: int = 0
        self.count = 0
        self._save_queue: mpq.Queue

    def start(self, pose_queue: mpq.Queue) -> Iterable[mp.Process]:
        """Initialize the CSVLogger.

        This needs to be done here instead of the init function \
            because of how windows multiprocessing works.

        Args:
            pose_queue (mpq.Queue): The queue where pose data \
                will be coming in.

        Returns:
            Iterable[mp.Process]: Any processes created by the \
                logger that will need to be cleaned up later.
        """
        self._save_queue = mp.Queue()
        cap = mp.Process(target=self._log_data, args=(
            pose_queue, self._save_queue))
        cap.start()
        return [cap]

    def _configure(self, size) -> None:
        # Add one to make room for the timestamp
        self.data = np.empty((0, size + 1))
        self.size = size

    def _log_data(self, pose_queue: mpq.Queue, save_queue: mpq.Queue) -> None:
        """Get data from queue and add it to the internal numpy array.

        Args:
            pose_queue (mpq.Queue): The queue of pose data coming in.
            save_queue (mpq.Queue): The queue to notify of when to save.
        """
        while True:
            if self.active:
                if pose_queue.empty():
                    continue

                pose_data: np.ndarray = pose_queue.get()
                newdata: np.ndarray = pose_data.ravel()

                # Create numpy array if not already created
                if self.data is None:
                    data_length: int = newdata.shape[0]
                    self._configure(data_length)

                # insert timestamp into first index
                newdata = np.insert(newdata, 0, [time.time()])
                self.data = np.vstack([self.data, newdata])

                # Save the data if the save queue has been pushed
                # to or if data hasn't been saved for 1 second.
                if not save_queue.empty():
                    save_queue.get()
                    self._save_to_csv()

    def _save_to_csv(self) -> None:
        header: str = self._build_header()
        np.savetxt(self.filepath, self.data, header=header,
                   delimiter=",", fmt="%5.5f", comments="")

    def _build_header(self) -> str:
        """
        Create the csv file header.

        This method assumes each pose point has 4 points \
            (x, y, z, visibility).
        """
        header_array: List[str] = []
        for i in range(self.size//4):
            header_array += [f"x{i:02d}", f"y{i:02d}",
                             f"z{i:02d}", f"vis{i:02d}"]
        return "timestamp," + ",".join(header_array)

    def save(self) -> None:
        """Write the most current data to the disk."""
        self._save_queue.put(0)

    def close(self) -> None:
        """Finish writing to the file."""
        self._save_queue.put(0)
        self.active = False
