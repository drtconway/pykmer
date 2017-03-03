"""
This module provides a simple timer class for instrumenting code.
"""

import time

class timer(object):
    def __init__(self):
        self.start = time.time()
        self.sofar = 0.0
        self.paused = False
        self.events = 0

    def pause(self):
        now = time.time()
        self.sofar += now - self.start
        self.paused = True

    def resume(self):
        self.start = time.time()
        self.paused = False

    def stop(self):
        if not self.paused:
            now = time.time()
            self.sofar += now - self.start

    def tick(self, n = 1):
        self.events += n

    def reset(self):
        self.start = time.time()
        self.sofar = 0
        self.paused = False

    def time(self):
        sofar = self.sofar
        if not self.paused:
            now = time.time()
            sofar += now - self.start
        return sofar

    def rate(self, n = None):
        if n is None:
            n = self.events
        return n / self.time()
