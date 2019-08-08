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
        
        self.target_pitch = 0
        self.target_roll = 0
        self.target_yaw = 0
        self.throttle = 0
        self.throttle_squared = 0

    def _parse_pitch(self, pid_output):
        # If positive pitch up
        front = math.sqrt(self.throttle_squared + pid_output)
        back = math.sqrt(self.throttle_squared - pid_output)
        return (front, back)

    def _parse_roll(self, pid_output):
        # If positive roll counter-clockwise
        right = math.sqrt(self.throttle_squared + pid_output)
        left = math.sqrt(self.throttle_squared - pid_output)
        return (right, left)
    
    def _parse_yaw(self, pid_output):
        # If positive yaw right
        # figure out which ones turns
        return 0

    def _eval_loop(self):
        while True:
            self.throttle_squared = self.throttle ** 2


    def start(self):
        self.computation_thread = threading.Thread(target=self._eval_loop)
        self.computation_thread.start()
