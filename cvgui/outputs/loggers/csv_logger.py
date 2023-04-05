import multiprocessing as mp

class CSVLogger:

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def start(self, mp.Queue) -> Iterable[mp.Process]:
        cap = mp.Process(target=self.log_data)
        return cap
    
    def log_data(self):
        # Create numpy array if not already created

        # Get data from queue and append it to numpy array
        pass
    
    def save(self):
        # Save data to CSV
        pass
    
    def close(self):
        # Finish writing to the file
        pass
