import pygame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("General Relativity Visualization")
clock = pygame.time.Clock()

# Function to draw the scene using Matplotlib
def draw_scene(ax):
    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)

    # Draw gravitational object
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 0.5 * np.outer(np.cos(u), np.sin(v))
    y = 0.5 * np.outer(np.sin(u), np.sin(v))
    z = 0.5 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='white')

    # Draw light rays and apply gravitational lensing
    angle = np.linspace(0, 2*np.pi, 100)
    for a in angle:
        x_start, y_start, z_start = 0, 0, -5
        x_end, y_end, z_end = 5 * np.cos(a), 5 * np.sin(a), 5
        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], color='yellow')
        x_end, y_end, z_end = calculate_bending(x_end - x_start, y_end - y_start, z_end - z_start, M)
        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], color='red')

# Define functions for gravitational lensing effect
def bending_angle(x, y, z, M):
    r = np.sqrt(x**2 + y**2 + z**2)
    return 4 * M / r

def calculate_bending(x, y, z, M):
    theta = bending_angle(x, y, z, M)
    x_new = x + theta * x / np.sqrt(x**2 + y**2 + z**2)
    y_new = y + theta * y / np.sqrt(x**2 + y**2 + z**2)
    z_new = z + theta * z / np.sqrt(x**2 + y**2 + z**2)
    return x_new, y_new, z_new

# Main loop
def main():
    running = True

    # Set up Matplotlib plot
    fig = plt.figure(figsize=(WIDTH/100, HEIGHT/100))
    ax = fig.add_subplot(111, projection='3d')

    while running:
        screen.fill(BLACK)

        # Draw scene using Matplotlib
        draw_scene(ax)
        plt.draw()
        plt.savefig('temp.png')  # Save Matplotlib figure to a temporary image

        # Load and display the temporary image using Pygame
        img = pygame.image.load('temp.png')
        screen.blit(img, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
