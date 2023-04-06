from pathlib import Path
from typing import Iterable, List
import numpy as np
import multiprocessing as mp


class CSVLogger:

    active: bool = True

    def __init__(self, filepath: Path) -> None:
        self.filepath: Path = filepath
        self.data: np.ndarray = np.empty((0, 132))
        self.size: int = 0
        self.count = 0

    def start(self, pose_queue: mp.Queue) -> Iterable[mp.Process]:
        self._save_queue: mp.Queue = mp.Queue()
        cap = mp.Process(target=self.log_data, args=(
            pose_queue, self._save_queue))
        cap.start()
        return [cap]

    def _configure(self, size) -> None:
        self.data = np.empty((0, size))
        self.size = size

    def log_data(self, pose_queue: mp.Queue, save_queue: mp.Queue) -> None:
        # Get data from queue and append it to numpy array
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

                self.data = np.vstack([self.data, newdata])

                if not save_queue.empty():
                    save_queue.get()
                    header: str = self._build_header()
                    np.savetxt(self.filepath, self.data, header=header,
                               delimiter=",", fmt="%5.5f")

    def _build_header(self) -> str:
        header_array: List[str] = []
        for i in range(self.size//4):
            header_array += [f"x{i:02d}", f"y{i:02d}",
                             f"z{i:02d}", f"vis{i:02d}"]
        return ",".join(header_array)

    def save(self) -> bool:
        # Notify the running process that it is time
        # to save.
        self._save_queue.put(0)
        return True

    def close(self) -> bool:
        # Finish writing to the file
        self._save_queue.put(0)
        self.active = False
        return True
