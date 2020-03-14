import time
import math
from typing import Tuple
import board
import adafruit_bno055
import busio

class IMU:

    def __init__(self) -> None:
        """
        Sets up sensor.
        Arguments: nothing
        Returns: nothing
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055(self.i2c)

    def check_calibration(self):
        """
        Checks calibration of sensor.
        Arguments: nothing
        Returns: dict of calibration statuses
        """
        values = self.sensor.calibration_status  # sys, gyro, accelerometer, mag
        keys = ["sys", "gyroscope", "accelerometer", "magnetometer"]
        return dict(zip(keys, values))

    def sample(self):
        """
        Queries sensor and returns euler angles (yaw, pitch, roll)
        """
        return self.sensor.quaternion # (x, y, z, w)
