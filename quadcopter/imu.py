import time
import math
from typing import Tuple
import board
import adafruit_bno055
import busio

def quaternion_to_euler(quaternion: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
    """
    Converts quaternion (x,y,z,w) to euler angles (yaw, pitch, roll)
    Arguments:
        q (Tuple): a 4-tuple containing (w,x,y,z) in quaternion units
    Returns: a 3-tuple containing (yaw, pitch, roll)
    """
    x, y, z, w = quaternion

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    return [yaw, pitch, roll]

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
        quaternion = self.sensor.quaternion # (x, y, z, w)
        return quaternion_to_euler(quaternion)
