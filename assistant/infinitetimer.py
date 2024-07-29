import threading
import time

class InfiniteTimer():
    """
    A Thread that executes infinitely, used to reset to idle position
    """
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = threading.Timer(self.t, self.handle_function)
        self.thread.daemon = True
        self.begin = time.time()

    def is_timer_on(self):
        if self.thread.is_alive() and not self.thread.finished.is_set():
            return True
        else:
            return False

    def handle_function(self):
        self.hFunction()
        self.thread.cancel()
        # self.thread = threading.Timer(self.t, self.handle_function)
        # self.thread.daemon = True
        # self.thread.start()

    def start(self, t = None, hFunction = None):
        if t is None and hFunction is None:
            self.thread = threading.Timer(self.t, self.handle_function)
            self.thread.daemon = True
        elif t is not None and hFunction is not None:
            self.thread.cancel()
            self.t = t
            self.hFunction = hFunction
            self.thread = threading.Timer(self.t, self.handle_function)
            self.thread.daemon = True
        else:
            print("Arguments not defined")
        self.thread.start()
        self.begin = time.time()

    def remaining(self):
        return self.t - (time.time() - self.begin)

    def cancel(self):
        self.thread.cancel()