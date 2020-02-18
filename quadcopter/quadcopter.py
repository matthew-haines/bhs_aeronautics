from typing import Dict
import pigpio
import os
import time
from motor import Motor
os.system("sudo pigpiod")
time.sleep(1)

class Quadcopter:
    """Wrapper for all functions of the Quadcopter system"""

    def __init__(self, motor_ports: Dict[str, int]):
        """
        Sets up quadcopter. \n
        Arguments: \n
            motor_ports Dict: a dict of the ports used by each motor e.g. {"front_left": 3} \n
        Returns: nothing
        """
        self.pi = pigpio.pi()
        self.motor_ports = motor_ports

        # Motor setup:
        self.front_left = Motor(self.motor_ports["front_left"], self.pi)
        self.front_right = Motor(self.motor_ports["front_right"], self.pi)
        self.back_left = Motor(self.motor_ports["back_left"], self.pi)
        self.back_right = Motor(self.motor_ports["back_right"], self.pi)

        self.motor_min = 1000
        self.motor_max = 2000

        self.motor_list = [self.front_left,
                           self.front_right, self.back_left, self.back_right]

        self.throttle = 0
         
    def _set_all(self, speed: int):
        """
        Sets the speed of all motors assigned to the quadcopter. \n
        Arguments: \n
            speed (int): the speed value \n
        Returns: nothing
        """
        for motor in self.motor_list:
            motor.throttle(speed)

        self.throttle = speed

    def calibrate_all(self):
        """
        Calibrates every motor. This needs to happen whenever a motor has been disconnected from \n
            a power source. \n
        Arguments: nothing \n
        Returns: nothing
    """
        print("disconnect battery and press Enter")
        input()
        self._set_all(self.motor_max)
        print("connect battery and press enter")
        input()
        time.sleep(2)
        self._set_all(self.motor_min)
        time.sleep(8)
        print("calibrated")

    def arm_all(self):
        """
        Arms every motor. \n
        Arguments: nothing \n
        Returns: nothing
        """
        print("disconnect the battery and press enter")
        input()
        self._set_all(self.motor_min)
        print("Connect the battery and press Enter")
        input()
        time.sleep(1)

    def control_all(self):
        """
        Simple manual control for basic testing. \n
        Arguments: nothing \n
        Returns: nothing
        """
        print("w/s to increase decrease speed, q/e to big increase/descrease")
        while True:
            inp = input()
            if inp == "w":
                self._set_all(self.throttle+10)
            elif inp == "s":
                self._set_all(self.throttle-10)
            elif inp == "q":
                self._set_all(self.throttle+100)
            elif inp == "e":
                self._set_all(self.throttle-100)
            elif inp == "stop":
                self._set_all(0)
            else:
                self._set_all(int(inp))


    
