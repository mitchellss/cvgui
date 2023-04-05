
class PoseLogger(Protocol):

    def start(self, pose_queue: mp.Queue) -> Iterable[mp.Process]:
        """
        Initializes the pose logger.
        """
