import pid
import motor
import math
import threading

class MotorHandler:

    def __init__(self, front: motor.Motor, left: motor.Motor, right: motor.Motor, back: motor.Motor):
        self.front = front 
        self.left = left
        self.right = right 
        self.back = back

        self.pitch_pid = pid.PID([1, 1, 1])
        self.roll_pid = pid.PID([1, 1, 1])
        self.yaw_pid = pid.PID([1, 1, 1])
        self.current_pitch = 0.0
        self.current_roll = 0.0
        self.current_yaw = 0.0
        self.target_pitch = 0.0
        self.target_roll = 0.0
        self.target_yaw = 0.0
        self.throttle = 0.0
        self.throttle_squared = 0.0

    def _eval_loop(self):
        # [yaw, pitch, roll]
        pitch_value = self.pitch_pid.step(self.current_pitch, self.target_pitch)
        roll_value = self.roll_pid.step(self.current_roll, self.target_roll)
        yaw_value = self.yaw_pid.step(self.current_yaw, self.target_yaw)

        self.front.throttle(int(math.sqrt(self.throttle_squared + pitch_value + yaw_value)))
        self.back.throttle(int(math.sqrt(self.throttle_squared - pitch_value, + yaw_value)))
        self.left.throttle(int(math.sqrt(self.throttle_squared + roll_value - yaw_value)))
        self.right.throttle(int(math.sqrt(self.throttle_squared - roll_value - yaw_value)))

    def start(self):
        threading.Thread(target=self._eval_loop)
