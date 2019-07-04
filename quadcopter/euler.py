from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

s = math.sin
c = math.cos

def rotate(x, euler, inverse=False):
    # vector, euler angles
    phi, theta, psi = euler[0], euler[1], euler[2]
    # z x' z" rotation matrix
    matrix = np.array([[c(phi)*c(psi) - c(theta)*s(phi)*s(psi), -c(phi)*s(psi)-c(theta)*c(psi)*s(phi), s(phi)*s(theta)],
                       [c(psi)*s(phi)+c(phi)*c(theta)*s(psi), c(phi)*c(theta)*c(psi)-s(phi)*s(psi), -c(phi)*s(theta)],
                       [s(theta)*s(psi), c(psi)*s(theta), c(theta)]])

    if inverse: 
        matrix = np.linalg.inv(matrix)

    out = np.dot(matrix, np.array(x))
    return out.tolist()

x = [0, 0, 1]
y = [0, 1, 0]
z = [1, 0, 0]

origin = [0, 0, 0]

euler = [3, 2, 1]  # phi, theta, psi (rad)

d, e, f = zip(origin, origin, origin)
U, V, W = zip(x, y, z)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)
ax.quiver(d, e, f, U, V, W, length=1.0, color='b')

x = rotate(x, euler)
y = rotate(y, euler)    
z = rotate(z, euler)

U, V, W = zip(x, y, z)
ax.quiver(d, e, f, U, V, W, length=1.0, color='r')
plt.show()

print(rotate(x, euler, inverse=True), rotate(y, euler, inverse=True), rotate(z, euler, inverse=True))