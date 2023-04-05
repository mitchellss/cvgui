import numpy as np
import multiprocessing as mp

class CSVLogger:

    data: np.ndarray
    size: int
    active: bool = True

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def start(self, pose_queue: mp.Queue) -> Iterable[mp.Process]:
        cap = mp.Process(target=self.log_data, args=pose_queue)
        return cap
    
    def _configure(self, size):
        self.data = np.empty((0,size))
        self.size = size
    
    def log_data(self, pose_queue: mp.Queue) -> None:
        # Get data from queue and append it to numpy array
        while self.active:
            if pose_queue.empty():
                continue
            pose_data = pose_queue.get()
            newdata = pose_data.ravel()

            # Create numpy array if not already created
            if self.data is None:
                data_length = newdata.shape[0]
                self._configure(data_length)

            self.data = np.vstack([self.data, newdata])
    
    def _build_header(self) -> str:
        header_array = []
        for i in range(self.size//4):
            header_array += [f"x{i:02d}",f"y{i:02d}",f"z{i:02d}",f"vis{i:02d}"]
        return ",".join(header_array)
    
    def save(self) -> bool:
        # Save data to CSV
        header = self._build_header()
        np.savetxt(self.filepath, self.data, header=header, delimiter=",", fmt="%5.5f")
    
    def close(self) -> bool:
        # Finish writing to the file
        self.active = False
