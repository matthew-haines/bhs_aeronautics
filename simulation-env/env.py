import torch
from math import cos, sin, pi

if torch.cuda.is_available():  # If GPU is available create tensors on GPU
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

def uniform_vector(m, n, min_value, max_value):
    return (min_value - max_value) * torch.rand(m, n) + max_value


class SimpleQuadcopterSimulation:
    """
    Environment that simulates quadcopter flight given input of a motor rpm vector  (ℝ⁴)
    """

    def __init__(self, **kwargs):

        self.params = {  # Default parameters
            "time": 10,  # seconds, simulation time
            "dt": 0.005,  # Δt between steps
            "mass": 1.5,  # kg
            "start_velocity": None,  # random
            "start_position": None,  # random
            "start_angle": None,  # random
            "start_angle_vel": None,  # random
            # "tpc": 1, # torque proportionality constant, specific to motor
            # "zero_current": 1, # current to each motor when load = 0
            # "back_emf": 1, # back emf generated per rpm (when motors run, they also generate emf, this reduces current flowing)
            "air_density": 1.225,  # kg/m³, at SATP
            "rotor_area": 10,  # cm²
            "gravity_accel": 9.80,  # m/s² at earth's surface
            "motor_distance": 5,  # cm from center of quadcopter to motor
            "k": 3e-6,  # constant used for torque calculations
            "kd": 0.25,  # constant for calculation of friction
            "L": 0.25, # distance from motors to center of quadcopter
            "b": 3e-6 # drag coefficient
        }
        for (param, val) in (self.params.iteritems()):  # replaces defaults parameters with user defined if exist
            setattr(self, param, kwargs.get(param, val))

        # Parameters needed for computations
        self.gravity = torch.t(
            torch.Tensor([0, 0, -self.params["gravity_accel"]])
        )  # Tranpose to column vector

        self.inertia = torch.diag([5e-3, 5e-3, 10e-3])

        self.reset()

    def reset(self):

        # State parameters
        self.velocity - self.params["start_velocity"]
        self.position = self.params["start_position"]
        self.angles = self.params["start_angle"]
        self.angular_velocity = self.params["start_angle_vel"]

        if self.params["start_velocity"] == None:
            self.velocity = uniform_vector(3, 1, -10, 10)
        if self.params["start_position"] == None:
            self.acceleration = torch.t(torch.Tensor([0, 0, 10]))
        if self.params["start_angle"] == None:
            self.angles = uniform_vector(3, 1, -2 * pi, 2 * pi)
        if self.params["start_angle_vel"] == None:
            self.angular_velocity = uniform_vector(
                3, 1, -2 * pi, 2 * pi
            )  # Rads/s², 1 rotation per s max

    def step(self, inputs):
        """
        Steps forward in the simulation, takes the s
        """
        omega = self.theta_dot_to_omega(self.angular_velocity, self.angles)
        a = self.compute_acceleration(inputs, self.angles, self.velocity, self.params['mass'], self.gravity, self.params['k'], self.params['kd'])
        omegadot = self.compute_angular_acceleration(inputs, omega, self.inertia, self.params['L'], self.params['b'], self.params['k'])

        omega = omega + self.params['dt'] * omegadot

        # Compute new state
        self.angular_velocity = self.omega_to_theta_dot(omega, self.angular_velocity)
        self.angles = self.angles + self.params['dt'] * self.angular_velocity
        self.velocity = self.velocity + self.params['dt'] * a
        self.position = self.position + self.params['dt'] * self.angular_velocity

        return (self.angles, self.angular_velocity, self.position, self.velocity)

    def theta_dot_to_omega(self, thetadot, angles):
        """
        Angles: A 3 size vector of the euler angles
        thetadot: A 3 size vector of the derivatives of roll, pitch, yaw with respect to time
        
        Returns: A angular velocity vector
        """
        phi = angles[0]
        theta = angles[1]
        psi = angles[2]

        matrix = torch.Tensor(
            [1, 0, -sin(theta)],
            [0, cos(phi), cos(theta) * sin(phi)],
            [0, -sin(phi), cos(theta) * cos(phi)],
        )
        return torch.dot(matrix, thetadot)

    def rotation(self, angles):
        """
        Function that creates a 3x3 rotation matrix from angle vectors of ℝ³ 
        """
        phi = angles[0]
        theta = angles[1]
        psi = angles[2]
        r_matrix = torch.zeros(3, 3)
        r_matrix[:, 0] = [cos(phi) * cos(theta), cos(theta) * sin(phi), -sin(theta)]
        r_matrix[:, 1] = [
            cos(phi) * sin(theta) * sin(psi) - cos(psi) * sin(phi),
            cos(phi) * cos(psi) + sin(phi) * sin(theta) * sin(psi),
            cos(theta) * sin(psi)
        ]
        r_matrix[:, 2] = [
            sin(phi) * sin(psi) + cos(phi) * cos(psi) * sin(theta),
            cos(psi) * sin(phi) * sin(theta) - cos(phi) * sin(psi),
            cos(theta) * cos(psi)
        ]
        return r_matrix 

    def thrust(self, inputs, k):
        return torch.t(torch.Tensor([0, 0, k * torch.sum(inputs)]))

    def compute_acceleration(self, inputs, angles, velocity, mass, gravity, k, kd):
        R = self.rotation(angles)
        T = torch.dot(R, self.thrust(inputs, k))
        Fd = -kd * velocity
        return gravity + 1 / mass * T + Fd

    def torques(self, inputs, L, b, k):
        return torch.t(torch.Tensor([L * k * (inputs[0] - inputs[2]), L * k * (inputs[1] - inputs[3]), 
                                    b * (inputs[0] - inputs[1] + inputs[2] - inputs[3])]))
                                    
    def compute_angular_acceleration(self, inputs, omega, I, L, b, k):
        tau = self.torques(inputs, L, b, k)
        return torch.inverse(I) * (tau - torch.cross(omega, I * omega))

    def compute_thrust(self, angular_velocity):
        return torch.t(torch.Tensor(0, 0, torch.t(angular_velocity).dot(angular_velocity)))

    def create_rotation_matrix(self, angles):
        """
        Function that creates a 3x3 rotation matrix from angle vectors of ℝ³ 
        """
        phi = angles[0]
        theta = angles[1]
        psi = angles[2]
        r_matrix = torch.zeros(3, 3)
        r_matrix[:, 0] = [cos(phi) * cos(theta), cos(theta) * sin(phi), -sin(theta)]
        r_matrix[:, 1] = [
            cos(phi) * sin(theta) * sin(psi) - cos(psi) * sin(phi),
            cos(phi) * cos(psi) + sin(phi) * sin(theta) * sin(psi),
            cos(theta) * sin(psi),
        ]
        r_matrix[:, 2] = [
            sin(phi) * sin(psi) + cos(phi) * cos(psi) * sin(theta),
            cos(psi) * sin(phi) * sin(theta) - cos(phi) * sin(psi),
            cos(theta) * cos(psi),
        ]
        return r_matrix

def main():
    sim = SimpleQuadcopterSimulation()

if __name__ == "__main__":
    main()
