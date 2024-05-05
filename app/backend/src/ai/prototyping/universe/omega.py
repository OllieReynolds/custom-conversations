import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Initialize the figure for animation
fig, ax = plt.subplots()
fig.set_tight_layout(True)
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.axis('off')  # Hide the axes

# Create initial positions for "galaxies" and stars
num_galaxies = 20
num_stars = 100
galaxy_positions = np.random.rand(num_galaxies, 2) * 12 - 6
star_positions = np.random.rand(num_stars, 2) * 12 - 6

galaxies = ax.scatter(galaxy_positions[:, 0], galaxy_positions[:, 1], s=200, c=np.random.rand(num_galaxies), cmap='rainbow', edgecolors='white', alpha=0.8)
stars = ax.scatter(star_positions[:, 0], star_positions[:, 1], s=10, c='white', alpha=0.5)

# Scale factors for different density parameters (Ω values)
time = np.linspace(0, 1, 400)
density_params = [0.5, 1, 1.5]  # Ω values
scale_factors = [np.power(time, 2 * omega / 3) for omega in density_params]

def update(frame_number):
    # Cycle through different density parameters
    omega_index = frame_number // 133 % len(density_params)
    scale_factor = scale_factors[omega_index][frame_number % 133]

    # Update galaxy positions based on the scale factor
    updated_galaxy_positions = (galaxy_positions - galaxy_positions.mean(0)) * scale_factor + galaxy_positions.mean(0)
    galaxies.set_offsets(updated_galaxy_positions)

    # Make stars twinkle
    if frame_number % 10 == 0:
        stars.set_sizes(np.random.rand(num_stars) * 20)

    # Update the title to show the current Ω value
    ax.set_title(f'Universe Expansion - Density Parameter Ω = {density_params[omega_index]:.1f}', fontsize=16, color='white')
    fig.patch.set_facecolor('black')
    ax.patch.set_facecolor('black')

# Create the animation
ani = FuncAnimation(fig, update, frames=400, interval=50)

plt.show()
