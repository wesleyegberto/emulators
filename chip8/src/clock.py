import time

from threading import Thread

class CancellationToken:
    canceled = False

class Clock(Thread):
    """
    Class to represent a clock as a thread.
    """
    canceled = False
    cancellation_token = CancellationToken()

    def __init__(self, task, clock_hz):
        super().__init__(target=self._start_clock)
        self.task = task
        self.clock_hz = clock_hz

    def cancel(self):
        self.canceled = True

    def _start_clock(self):
        while True:
            if self.canceled:
                break
            self.task()
            time.sleep(1 / self.clock_hz)

