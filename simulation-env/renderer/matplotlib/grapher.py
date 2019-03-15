import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import torch
from numpy import sin, cos


class Grapher:

    def __init__(self, xlim, ylim, zlim):

        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection='3d'))

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_zlim(zlim)

    def update(position, angles):
        """
        Position is a torch vector of the xyz coordinates of the quadcopter
        Angles is a torch vector of the angles relative to the ground in radians
        """
        xyz = position.tolist()
        pitch = angles[0]
        roll = angles[1]
        yaw = angles[2]
        # http://planning.cs.uiuc.edu/node102.html for Rotation matrix
        # Order matters here so this might be an issue
        rotational_matrix = torch.Tensor([cos(yaw)*cos(pitch), cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll), cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll)],
                                         [sin(yaw)*cos(pitch), sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(
                                             roll), sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll)],
                                         [-sin(pitch), cos(pitch)*sin(roll), cos(pitch)*cos(roll)])

        unit_vector = torch.dot(rotational_matrix, torch.Tensor([0], [0], [1]))
        
