import sys
import numpy as np

class Simulation:

    def __init__(self, render=False):
        # All units in SI
        # Constants
        self.mass = 0.5
        self.motor_distance = 0.4
        self.motor_constant = 3e-6
        self.yaw_constant = 1e-7
        self.drag_constant = 0.25
        self.gravity = 9.80665
        self.inertia = np.diag([5e-3, 5e-3, 10e-3])  # moment of inertia
        self.inertia_inv = np.linalg.inv(self.inertia)
        self.gravity_force = np.array([0.0, 0.0, -self.mass * self.gravity])
        self.dt = 1e-3

        # State
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        self.rotation = np.zeros(3)
        self.angular_velocity = np.zeros(3)

    def _rotational_matrix(self):
        # body frame to inertial frame
        s = np.sin
        c = np.cos
        r = self.rotation[0]
        p = self.rotation[1]
        y = self.rotation[2]
        return np.array([[c(r)*c(y)-c(p)*s(r)*s(y), -c(y)*s(r)-c(r)*c(p)*c(y), s(p)*s(y)],
                         [c(p)*c(y)*s(r)+c(r)*s(y), c(r)*c(p)*c(y)-s(r)*s(y), -c(y)*s(p)],
                         [s(r)*s(p), c(r)*s(p), c(p)]])

    def _angular_velocity_matrix(self):
        # Rotation axis = this * angular velocities (euler angles)
        s = np.sin
        c = np.cos
        r = self.rotation[0]
        p = self.rotation[1]
        return np.array([[1, 0, -s(p)],
                         [0, c(r), c(p)*s(r)],
                         [0, -s(r), c(p)*c(r)]])

    def _calculate_torques(self, propeller_speeds):
        # returns torque vector in body frame (roll, pitch, yaw)
        roll_torque = self.motor_distance * self.motor_constant * \
            (propeller_speeds[0] ** 2 - propeller_speeds[2] ** 2)
        pitch_torque = self.motor_distance * self.motor_constant * \
            (propeller_speeds[1] ** 2 - propeller_speeds[3] ** 2)
        yaw_torque = self.yaw_constant * \
            np.dot(np.array([1.0, -1.0, 1.0, -1.0]) *
                   propeller_speeds, propeller_speeds)
        return np.array([roll_torque, pitch_torque, yaw_torque])

    def rotation_quaternion(self):
        # q = [x, y, z, w]
        s = np.sin
        c = np.cos
        r = self.rotation[0]
        p = self.rotation[1]
        y = self.rotation[2]
        return np.array([
            s(r)*c(p)*c(y)-c(r)*s(p)*s(y),
            c(r)*s(p)*c(y)+s(r)*c(p)*s(y),
            c(r)*c(p)*s(y)-s(r)*s(p)*c(y),
            c(r)*c(p)*c(y)+s(r)*s(p)*s(y)
        ])

    def step(self, propeller_speeds):
        rotational_matrix = self._rotational_matrix()
        thrust = np.array([0, 0, self.motor_constant * np.dot(propeller_speeds, propeller_speeds)])
        drag_force = -self.drag_constant * self.velocity
        linear_acceleration = (
            self.gravity_force + rotational_matrix @ thrust + drag_force) / self.mass
        self.velocity += self.dt * linear_acceleration
        self.position += self.dt * self.velocity

        torques = self._calculate_torques(propeller_speeds)
        angular_acceleration = self.inertia_inv @ (
            torques - np.cross(self.angular_velocity, self.inertia @ self.angular_velocity))
        angular_velocity_matrix = self._angular_velocity_matrix()
        angular_velocity_axis = angular_velocity_matrix @ self.angular_velocity
        angular_velocity_axis += self.dt * angular_acceleration
        self.angular_velocity = np.linalg.inv(angular_velocity_matrix) @ angular_velocity_axis
        self.rotation += self.dt * self.angular_velocity
