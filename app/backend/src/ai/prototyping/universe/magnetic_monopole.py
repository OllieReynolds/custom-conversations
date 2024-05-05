import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Magnetic Field Simulation")
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Text rendering function
def render_text(text, pos, size=30, color=black):
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

# Define states for different parts of the animation
states = ['dipole', 'dipole_text', 'monopole', 'monopole_text', 'ending_text']
state_index = 0

# Time spent on each state (in seconds)
state_durations = [8, 4, 8, 4, 4]
state_timer = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill(white)

    # Calculate elapsed time in seconds
    elapsed_time = clock.tick(60) / 1000.0
    state_timer += elapsed_time

    # Check if it's time to switch state
    if state_timer >= state_durations[state_index]:
        state_timer = 0
        state_index = (state_index + 1) % len(states)
    
    current_state = states[state_index]

    # Dipole state
    if current_state == 'dipole':
        for angle in range(0, 360, 10):
            z = 200 * math.cos(math.radians(angle) + pygame.time.get_ticks() * 0.002)
            y = 200 * math.sin(math.radians(angle) + pygame.time.get_ticks() * 0.002)
            x = 0
            pygame.draw.circle(screen, blue, (int(width / 2 + x), int(height / 2 + y)), int(200 / (z / 200)), 2)

    # Dipole text state
    elif current_state == 'dipole_text':
        render_text("This is a dipole field", (width / 2, height / 2), 40, blue)

    # Monopole state
    elif current_state == 'monopole':
        for angle in range(0, 360, 10):
            z = 200 * math.cos(math.radians(angle) - pygame.time.get_ticks() * 0.002)
            y = 200 * math.sin(math.radians(angle) - pygame.time.get_ticks() * 0.002)
            x = 0
            pygame.draw.circle(screen, red, (int(width / 2 + x), int(height / 2 + y)), int(200 / (z / 200)), 2)

    # Monopole text state
    elif current_state == 'monopole_text':
        render_text("This is a hypothetical monopole field", (width / 2, height / 2), 40, red)

    # Ending text state
    elif current_state == 'ending_text':
        render_text("Monopoles have not been observed in nature", (width / 2, height / 2 - 30), 30)
        render_text("Their existence would have profound implications", (width / 2, height / 2 + 30), 30)

    # Refresh screen
    pygame.display.flip()

pygame.quit()
sys.exit()
