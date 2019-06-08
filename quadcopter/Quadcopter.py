from typing import Dict
import pigpio
import os
import time
os.system("sudo pigpiod")
time.sleep(1)


class Motor:
    """Simple wrapper for an ESC motor"""

    def __init__(self, pin: int, pi: pigpio.pi, motor_max=700, motor_min=2000):
        """
        Sets up motor. \n
        Arguments: \n
            pin (int): the GPIO pin the motor is connected to \n
            pi (pigpio.pi): the instance of the pigpio class being used \n
            motor_max (int): the maximum setting for the motor \n
            motor_min (int): the minimum setting for the motor \n
        Returns: nothing
        """
        self.pin = pin
        assert isinstance(
            pi, pigpio.pi), "pi object is of type: {}, not pigpio.pi".format(type(pi))
        self.pi = pi

        self.motor_max = motor_max
        self.motor_min = motor_min

        self.current_value = 0

    def throttle(self, speed: int):
        """
        Changes throttle of motor to desired speed. \n
        Arguments: \n
            Speed (int): the speed value \n
        Returns: nothing
        """
        self.pi.set_servo_pulsewidth(self.pin, speed)
        self.current_value = speed

    def calibrate(self):
        """
        Calibration for just this motor, only used for testing purposes. \n
        Arguments: nothing \n
        Returns: nothing
        """
        self.throttle(0)
        print("disconnect battery and press Enter")
        input()
        self.throttle(self.motor_max)
        print("Connect the battery now. After it finishes beeping press Enter")
        input()
        self.throttle(self.motor_min)
        time.sleep(12)
        self.throttle(0)
        time.sleep(2)
        self.throttle(self.motor_min)

    def arm(self):
        """
        Arming for just this motor, only used for testing purposes. \n
        Arguments: nothing \n
        Returns: nothing
        """
        print("Connect the battery and press Enter")
        input()
        self.throttle(0)
        time.sleep(1)
        self.throttle(self.motor_max)
        time.sleep(1)
        self.throttle(self.motor_min)
        time.sleep(1)

    def manual_control(self):
        """
        Simple manual control loop for basic testing. \n
        Arguments: None \n
        Returns: None
        """
        print("w/s to increase decrease speed, q/e to big increase/descrease")
        while (True):
            inp = input()
            if inp == "w":
                self.throttle(self.current_value+10)
            elif inp == "s":
                self.throttle(self.current_value-10)
            elif inp == "q":
                self.throttle(self.current_value+100)
            elif inp == "e":
                self.throttle(self.current_value-100)
            elif inp == "stop":
                self.throttle(0)
            else:
                self.throttle(int(inp))


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
        self.front_left = Motor(self.motor_ports['front_left'], self.pi)
        self.front_right = Motor(self.motor_ports['front_right'], self.pi)
        self.back_left = Motor(self.motor_ports['back_left'], self.pi)
        self.back_right = Motor(self.motor_ports['back_right'], self.pi)

        self.motor_min = 700
        self.motor_max = 2000

        self.motor_list = [self.front_left,
                           self.front_right, self.back_left, self.back_right]

    def _set_all(self, speed):
        """
        Sets the speed of all motors assigned to the quadcopter. \n
        Arguments: \n
            speed (int): the speed value \n
        Returns: nothing
        """
        for motor in self.motor_list:
            motor.throttle(speed)

    def calibrate_all(self):
        """
        Calibrates every motor. This needs to happen whenever a motor has been disconnected from \n
            a power source. \n
        Arguments: nothing \n
        Returns: nothing
        """
        self._set_all(0)
        print("Disconnect battery and press Enter")
        input()
        self._set_all(self.motor_max)
        print("Connect the battery now. After it finishes beeping press Enter")
        input()
        self._set_all(self.motor_min)
        time.sleep(12)
        self._set_all(0)
        time.sleep(2)
        self._set_all(self.motor_min)

    def arm_all(self):
        """
        Arms every motor. \n
        Arguments: nothing \n
        Returns: nothing
        """
        self._set_all(0)
        time.sleep(1)
        self._set_all(self.motor_max)
        time.sleep(1)
        self._set_all(self.motor_min)
        time.sleep(1)
