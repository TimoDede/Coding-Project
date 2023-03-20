# importing numpy package
import numpy as np
# importing matplotlib package
import matplotlib.pyplot as plt

# Creating an empty canvas(figure)
fig = plt.figure()

# Using the gca function, we are defining
# the current axes as a 3D projection
ax = fig.add_subplot(projection='3d')

# Labelling X-Axis
ax.set_xlabel('X-Axis')

# Labelling Y-Axis
ax.set_ylabel('Y-Axis')

# Labelling Z-Axis
ax.set_zlabel('Z-Axis')

# Creating 100 values for X
# in between 0 and 1
x = np.linspace(0, 1, 10)

# Creating 100 values for Y
# in between 0 and 1
y = np.linspace(0, 1, 10)

# Creating a sine curve
z = np.sin(x * 2 * np.pi) / 2 + 0.5

# zdir='z' fixes all the points to zs=0 and
# (x,y) points are plotted in the x-y axis
# of the graph
ax.plot(x, y, zs=0, zdir='z')

# zdir='y' fixes all the points to zs=0 and
# (x,y) points are plotted in the x-z axis of the
# graph
ax.plot(x, y, zs=0, zdir='y')

# zdir='z' fixes all the points to zs=0 and
# (x,z) points are plotted in the x-y axis of
# the graph
ax.plot(x, z, zs=0, zdir='z')

# Showing the above plot
plt.show()
