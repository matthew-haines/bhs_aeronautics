import keyboard as kb
import pigpio
import smbus
import numpy as np
import RPi.GPIO as gpio
import os
import time
os.system('sudo pigpiod')
time.sleep(1)

class motor_controller():

    def __init__(self, pi, pin_fl, pin_fr, pin_bl, pin_br, max_value=2800, min_value=800):

        self.pi = pi

        self.motors = {'fl': pin_fl, 'fr': pin_fr, 'bl': pin_bl, 'br': pin_br}

        self.max_value = max_value
        self.min_value = min_value

    def set_all(self, pulse_width):

        for motor in self.motors:
            self.pi.set_servo_pulsewidth(motor, pulse_width)

    def set(self, speeds):

        for motor, speed, in zip(self.motors, speeds):
            self.pi.set_servo_pulsewidth(motor, speed)

    def calibrate(self):

        print("Remove propellers")

        self.set_all(0)
        input("Disconnect battery and continue")

        self.set_all(self.max_value)
        input("Reconnect battery and continue")

        self.set_all(self.min_value)
        time.sleep(12)
        self.set_all(0)
        time.sleep(2)
        self.set_all(self.min_value)
        time.sleep(1)
        print("Calibration Complete")

    def update_pitch(self, directional_speeds, motor_speeds):
        motor_speeds['fl'] += directional_speeds['f']
        motor_speeds['fr'] += directional_speeds['f']
        motor_speeds['bl'] += directional_speeds['b']
        motor_speeds['br'] += directional_speeds['b']

        return motor_speeds

    def update_roll(self, directional_speeds, motor_speeds):
        motor_speeds['fl'] += directional_speeds['l']
        motor_speeds['fr'] += directional_speeds['l']
        motor_speeds['bl'] += directional_speeds['r']
        motor_speeds['br'] += directional_speeds['r']

        return motor_speeds

    def update_yaw(self, motor_speeds, value):
        motor_speeds['fl'] -= value
        motor_speeds['br'] -= value
        motor_speeds['fr'] += value
        motor_speeds['bl'] += value

        return motor_speeds

    def manual_control(self, update_value=5):
        """Control quadcopter with WS for pitch, AD for roll, QE for yaw, shift & control for throttle"""
        time.sleep(1)
        directional_speeds = {'f': 0, 'l': 0, 'r': 0, 'b': 0}
        motor_speeds = {'fl': self.min_value, 'fr': self.min_value,
                        'bl': self.min_value, 'br': self.min_value}
        while True:

            self.set(motor_speeds)

            if kb.is_pressed('w'):
                directional_speeds['f'] -= update_value
                directional_speeds['b'] += update_value
                motor_speeds = self.update_pitch(directional_speeds, motor_speeds)

            elif kb.is_pressed('s'):
                directional_speeds['f'] += update_value
                directional_speeds['b'] -= update_value
                motor_speeds = self.update_pitch(directional_speeds, motor_speeds)

            elif kb.is_pressed('a'):
                directional_speeds['l'] -= update_value
                directional_speeds['r'] += update_value
                motor_speeds = self.update_roll(directional_speeds, motor_speeds)

            elif kb.is_pressed('d'):
                directional_speeds['l'] += update_value
                directional_speeds['r'] -= update_value
                motor_speeds = self.update_roll(directional_speeds, motor_speeds)

            elif kb.is_pressed('shift'):
                for speed in motor_speeds:
                    speed += update_value

            elif kb.is_pressed("ctbl"):
                for speed in motor_speeds:
                    speed -= update_value

            elif kb.is_pressed('q'):
                motor_speeds = self.update_yaw(motor_speeds, update_value / 2)

            elif kb.is_pressed('e'):
                motor_speeds = self.update_yaw(motor_speeds, -update_value / 2)
            
            elif kb.is_pressed("q+p"):
                return

    def safe_landing(self):
        a = np.zeros((3, 1))
        v_t1 = np.zeros((3, 1))
        v_t2 = np.zeros((3, 1))
        delta_t = 1
        v_t2 = v_t1 + a * delta_t
        
        speed = np.linalg.norm(v_t2)

    def arm(self):
        input("Connect battery")
        self.set_all(0)
        time.sleep(1)
        self.set_all(self.max_value)
        time.sleep(1)
        self.set_all(self.min_value)
        
    def stop(self):
        self.set_all(0)
        self.pi.stop()
