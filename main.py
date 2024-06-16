import pygame
import math

# Define constants
WIDTH, HEIGHT = 1200, 800
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth and Moon Simulation")

# Scaling factors
DISTANCE_SCALE = 1 / 5000  # 1 pixel = 5,000 km
SIZE_SCALE = 1 / 1000  # 1 pixel = 1,000 km

# Gravitational constant (in km^3 kg^-1 s^-2)
G = 6.67430e-20

class Body:
    def __init__(self, name, color, diameter_km, distance_km, orbital_period_days, mass_kg):
        self.name = name
        self.color = color
        self.radius = diameter_km * SIZE_SCALE / 2
        self.distance = distance_km * DISTANCE_SCALE
        self.orbital_period = orbital_period_days
        self.angle = 0  # Initial angle for orbiting
        self.mass = mass_kg

        # Initial velocity components
        self.vx = 0
        self.vy = 0

    def update_position(self, time_increment, other_body):
        # Calculate distance between bodies
        dx = other_body.distance * math.cos(other_body.angle) - self.distance * math.cos(self.angle)
        dy = other_body.distance * math.sin(other_body.angle) - self.distance * math.sin(self.angle)
        distance = math.sqrt(dx**2 + dy**2)

        # Calculate gravitational force
        if distance > 0:
            force = G * self.mass * other_body.mass / distance**2
            acceleration = force / self.mass
            # Calculate acceleration components
            ax = acceleration * dx / distance
            ay = acceleration * dy / distance

            # Update velocity components
            self.vx += ax * time_increment
            self.vy += ay * time_increment

            # Update position components
            self.distance += self.vx * time_increment
            self.angle += math.atan2(self.vy, self.vx) * time_increment

    def draw(self, surface, center_x, center_y):
        # Calculate the body's position
        x = center_x + self.distance * math.cos(self.angle)
        y = center_y + self.distance * math.sin(self.angle)
        pygame.draw.circle(surface, self.color, (int(x), int(y)), int(self.radius))

class EarthMoonSystem:
    def __init__(self):
        self.bodies = []
        self.time_increment = 0.01  # Increment for updating positions

    def add_body(self, body):
        self.bodies.append(body)

    def update(self):
        # Update positions of all bodies
        for i, body in enumerate(self.bodies):
            # For each body, update its position influenced by other bodies
            for other_body in self.bodies[:i] + self.bodies[i+1:]:
                body.update_position(self.time_increment, other_body)

    def draw(self, surface):
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        # Draw the bodies
        for body in self.bodies:
            body.draw(surface, center_x, center_y)

# Create the Earth-Moon system
earth_moon_system = EarthMoonSystem()
# Add Earth (stationary in this simplified model)
earth_moon_system.add_body(Body("Earth", (0, 0, 255), 12742, 0, 0, 5.972e24))  # Earth mass in kg
# Add Moon orbiting Earth
earth_moon_system.add_body(Body("Moon", (200, 200, 200), 3474, 384400, 27.3, 7.342e22))  # Moon mass in kg

# Main loop
run = True
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the Earth-Moon system
    earth_moon_system.update()

    # Draw everything
    window.fill(BLACK)
    earth_moon_system.draw(window)
    pygame.display.update()

pygame.quit()
