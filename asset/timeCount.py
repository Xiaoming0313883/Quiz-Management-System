import time

class TimeCount(object):
    def __init__(self):
        self.start_time, self.stop_time = None, None

    def start(self):
        self.start_time = time.time()
        return self

    def stop(self):
        self.stop_time = time.time()
        return self

    def time(self):
        return self.stop_time - self.start_time

    def broadcast(self):
        print(f"Execution time: {self.time():.4f} seconds")