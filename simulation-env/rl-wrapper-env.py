import torch
from env import SimpleQuadcopterSimulation

class Environment:

    def __init__(self):

        self.parameters = {
            "time": 10,  # s
            "dt": 0.005,  # s
            "mass": 1.5,  # kg
            "start_velocity": None,
            "start_position": None,
            "start_angle": None,
            "start_angle_vel": None,
            "air_density": 1.225,  # kg/m³
            "rotor_area": 10,  # cm²
            "gravity_accel": 9.81,  # m/s² 
            "motor_distance": 5,  # cm
            "k": 3e-6,  # constant used for torque calculation
            "kd": 0.25,  # constant for calculation of friction
            "L": 0.25, # distance from motors to center of quadcopter
            "b": 3e-6 # drag coefficient
        }

        self.simulation = SimpleQuadcopterSimulation(**self.parameters)

    def reset(self):

        self.simulation.reset()
        self.last_velocity = self.simulation.velocity 
        self.last_angular_velocity = self.simulation.angular_velocity 

    def step(self, inputs):
        # inputs should be in voltage sent to ESCs
        rpm = self.convert_voltage_to_rpm(inputs)
        angles, angular_velocity, position, velocity = self.simulation.step(rpm)
        reward = torch.sum(self.last_velocity - velocity) + torch.sum(self.last_angular_velocity, angular_velocity)
        self.last_velocity = velocity
        self.last_angular_velocity = angular_velocity
        return reward

    def convert_voltage_to_rpm(self, rpms):
        # do some stuff
        return