import numpy as np 
from typing import List
import time

class PID:
    """
    PID Controller for Quadcopter
    """
    def __init__(self, coefficients: List):
        """
        """
        self.error = 0  
        self.last_error = 0
        self.error_integral = 0
        self.error_derivative = 0
        self.target = None

        self.kp, self.ki, self.kd = coefficients

        self.last_time = 0.0

    def step(self, actual, target):
        cur_time = time.time()
        error = target - actual
        self.target = target
        self.error = error
        dt = cur_time - self.last_time
        result = 0.0
        result += self.error * self.kp

        self.error_integral += ((self.error + self.last_error) / 2) * dt
        result += self.error_integral * self.ki

        self.error_derivative = (self.error - self.last_error) / dt
        result += self.error_derivative * self.kd

        self.last_time = cur_time
        self.last_error = error
        return result 
