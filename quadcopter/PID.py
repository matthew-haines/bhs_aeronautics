import numpy as np 
from typing import List
import time
import threading

class PID:
    """
    PID Controller for Quadcopter
    """
    def __init__(self, coefficients: List, p=True, i=True, d=True):
        """
        """
        self.coefficients = coefficients
        self.error = 0  
        self.last_error = 0
        self.error_integral = 0
        self.error_derivative = 0
        self.target = None

        self.p, self.i, self.d = p, i, d

        self.last_time = 0.0

    def step(self, actual, target):
        cur_time = time.time()
        error = target - actual
        if target != self.target:
            self.last_error = error
            self.error_integral = 0
            self.last_time = cur_time
            self.target = target
            return 0

        self.target = target
        self.error = error
        dt = cur_time - self.last_time
        result = 0.0
        if self.p:
            result += self.error

        if self.i:
            self.error_integral += ((self.error + self.last_error) / 2) * dt
            result += self.error_integral

        if self.d:
            self.error_derivative = (self.error - self.last_error) / dt
            result += self.error_derivative

        self.last_time = cur_time
        self.last_error = error
        return result 
