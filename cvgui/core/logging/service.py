import multiprocessing as mp

class PoseLogger(Protocol):

    def start(self, pose_queue: mp.Queue) -> Iterable[mp.Process]:
        """
        Initializes the pose logger.
        """

    def log_data(self, pose_queue: mp.Queue) -> None:
        """
        Log data from the queue.
        """
    
    def save(self) -> bool:
        """
        Save logged data to the disk.
        """
    
    def close(self) -> bool:
        """
        Finish logging poses and safely close any
        files or repositories.
        """