import board
import busio
import adafruit_bno055
import time
from math import sin, cos, atan2, asin
from typing import Tuple
import numpy as np
import threading

class IMU:

    def __init__(self):
        """
        Sets up sensor.
        Arguments: nothing
        Returns: nothing
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055(self.i2c)

        self.accelerations = []
        self.headings = []
        self.acceleration = np.zeros(3)
        self.heading = np.zeros(3)
        
        # Time keeping for accuracy
        self.start_time = 0.0
        self.last_time = 0.0 # Last time computation was done for computing integrals
        self.times = []
        self.times_taken = []

        # Threading
        self.computation_thread = None
        self.stopped = False

    def check_calibration(self):
        """
        Checks calibration of sensor.
        Arguments: nothing
        Returns: dict of calibration statuses
        """
        values = self.sensor.calibration_status  # sys, gyro, accelerometer, mag
        keys = ["sys", "gyroscope", "accelerometer", "magnetometer"]
        return dict(zip(keys, values))

    def _round_to_half(self, x):
        return np.around(2.0 * x) / 2.0

    def _rotation_matrix(self, euler_angles: np.ndarray, moving_to_fixed=True):
        """
        Creates a rotation matrix for z y' x" order (yaw, pitch, roll)
        Arguments: 
            euler_angles (np.array): 3-tuple of euler angles in order (roll, pitch, yaw)
            moving_to_fixed (bool): Whether the rotating matrix is going from moving reference frame to fixed or the opposite
        Returns:
            np.array: 3x3
        """
        yaw = euler_angles[2]
        pitch = euler_angles[1]
        roll = euler_angles[0]

        s1 = sin(yaw)
        s2 = sin(pitch)
        s3 = sin(roll)
        c1 = cos(yaw)
        c2 = cos(pitch)
        c3 = cos(roll)

        rotation_matrix = np.array([[c1*c2, c1*s2*s3-c3*s1, s1*s3+c1*c3*s2],
                                    [c2*s1, c1*c3+s1*s2*s3, c3*s1*s2-c1*s3],
                                    [-s2, c2*s3, c2*c3]])

        if moving_to_fixed:
            rotation_matrix = np.linalg.inv(rotation_matrix)

        return rotation_matrix

    def _quaternion_to_euler(self, q: Tuple):
        """
        Converts quaternion (w,x,y,z) to euler angles (pitch, roll, yaw)
        Arguments:
            q (Tuple): a 4-tuple containing (w,x,y,z) in quaternion units
        Returns: a 3-tuple containing (pitch, roll, yaw)
        """
        # From DJI
        q2sqr = q[2] ** 2
        t0 = -2.0 * (q2sqr + q[3] ** 2) + 1.0
        t1 = 2.0 * (q[1] * q[2] + q[0] * q[3])
        t2 = -2.0 * (q[1] * q[3] - q[0] * q[2])
        t3 = 2.0 * (q[2] * q[3] + q[0] * q[1])
        t4 = -2.0 * (q[1] ** 2 + q2sqr) + 1.0

        t2 = 1.0 if t2 > 1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2

        pitch = asin(t2)
        roll = atan2(t3, t4)
        yaw = atan2(t1, t0)
        return (pitch, roll, yaw)


    def _main_loop(self, target_dt, verbose=False):
        """
        Main sensor polling and computation loop, should be run in its own thread.
        Arguments:
            dt (float): time delay between loops
            compute_integrals (bool): Whether or not to compute/log position/velocity
            verbose (bool): Adds verbosity (lots)
        Returns: nothing
        """
        i = 0
        while True:
            if self.stopped:
                return

            # self.heading = np.around(np.array(self.sensor.euler), decimals=0)
            self.heading = self._quaternion_to_euler(self.sensor.quaternion)
            # moving_frame_accel = np.array(self.sensor.linear_acceleration)
            cur_time = time.time()
            dt = cur_time - self.last_time  # in seconds
            self.times_taken.append(dt)
            # self.acceleration = self._round_to_half(np.dot(self._rotation_matrix(self.heading), moving_frame_accel))
            # self.headings.append(self.heading)
            # self.accelerations.append(self.acceleration)

            if verbose and ((i % 100) == False):
                print("Time: {}, Heading: {}".format(
                    round(cur_time-self.start_time, 3), self.heading))

            self.last_time = cur_time
            # self.times.append(cur_time - self.start_time)
            i += 1


    def start(self, polling_frequency: float = 100, verbose=False):
        """
        Starts the main computation loop.
        Arguments: 
            polling_frequency (float): Times sensor is polled per second (Hz)
            compute_integrals (bool): Whether or not to compute/log position/velocity
            verbose (bool): Adds verbosity (lots)
        Returns: nothing
        """
        polling_frequency = polling_frequency
        # assert polling_frequency <= 100, "{} > 100".format(polling_frequency)

        target_dt = 1 / polling_frequency

        self.computation_thread = threading.Thread(target=self._main_loop, args=[target_dt], kwargs={"verbose": verbose})
        self.start_time = time.time()
        self.last_time = self.start_time
        self.computation_thread.start()
        return

    def stop(self):
        """
        Stops the main computation loop.
        Arguments: nothing
        Returns: nothing
        """
        self.stopped = True
        return

    def write(self, path):
        """
        Writes telemetry data to a csv file.
        Arguments:
            path (string): The path to the file
        Returns: nothing
        """
        import csv
        with open(path, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(["Time (s)", "Acceleration (m/s²)", "Heading (roll, pitch, yaw) (deg)"])
            data_series = [self.accelerations, self.headings]
            # convert to strings
            for series in data_series:
                for i in series:
                    i = np.array2string(i)

            data_series.insert(0, self.times)
            rows = zip(data_series)
            for row in rows:
                writer.writerow(row)

        
