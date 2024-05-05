import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

# Setting up the figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_xlim([-6, 6])
ax.set_ylim([-6, 6])
ax.set_zlim([-6, 6])

# Sphere representing the universe
sphere = ax.plot_surface([], [], [], color='blue', alpha=0.6)

# Stars background in 3D
stars_x = np.random.uniform(-6, 6, 100)
stars_y = np.random.uniform(-6, 6, 100)
stars_z = np.random.uniform(-6, 6, 100)
ax.scatter(stars_x, stars_y, stars_z, c='white', alpha=0.5)

# Initialization function for the animation
def init():
    global sphere
    sphere.remove()
    sphere = ax.plot_surface([], [], [], color='blue', alpha=0.6)
    return sphere,

# Update function for the animation
def update(frame):
    global sphere
    sphere.remove()
    
    # Create a sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 0.5 * frame * np.outer(np.cos(u), np.sin(v))
    y = 0.5 * frame * np.outer(np.sin(u), np.sin(v))
    z = 0.5 * frame * np.outer(np.ones(np.size(u)), np.cos(v))

    # Update the sphere's size and color
    sphere = ax.plot_surface(x, y, z, color=plt.cm.viridis(frame % 256 / 256), alpha=0.6)
    return sphere,

# Creating the animation
ani = FuncAnimation(fig, update, frames=np.arange(1, 10, 0.1), init_func=init, blit=False, interval=100)

plt.show()
