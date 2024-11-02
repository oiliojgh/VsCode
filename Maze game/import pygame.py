import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Pac-Man settings
PACMAN_RADIUS = 20
PACMAN_SPEED = 3
PACMAN_MOUTH_SPEED = 0.1

# Pellet settings
PELLET_RADIUS = 5
PELLET_SCORE = 10

# Game settings
GAME_SPEED = 60  # frames per second
GAME_OVER_DELAY = 2  # seconds

# Load sounds
pac_man_chomp_sound = pygame.mixer.Sound("pac_man_chomp.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Game objects
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PACMAN_RADIUS
        self.speed = PACMAN_SPEED
        self.mouth_open = 0

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.mouth_open += PACMAN_MOUTH_SPEED
        if self.mouth_open >= 0.8 or self.mouth_open <= 0.2:
            PACMAN_MOUTH_SPEED *= -1

    def draw(self):
        pygame.draw.circle(window, YELLOW, (int(self.x), int(self.y)), self.radius)
        mouth_start = (self.x, self.y)
        mouth_end = (self.x + self.radius * (0.7 - self.mouth_open / 2), self.y)
        pygame.draw.line(window, BLACK, mouth_start, mouth_end, 2)

class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PELLET_RADIUS

    def draw(self):
        pygame.draw.circle(window, WHITE, (int(self.x), int(self.y)), self.radius)

# Game loop
def game_loop():
    pacman = PacMan(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    pellets = []

    # Create pellets
    for i in range(50):
        x = random.randint(PELLET_RADIUS, WINDOW_WIDTH - PELLET_RADIUS)
        y = random.randint(PELLET_RADIUS, WINDOW_HEIGHT - PELLET_RADIUS)
        pellet = Pellet(x, y)
        pellets.append(pellet)

    score = 0
    game_over = False
    game_over_timer = 0

    clock = pygame.time.Clock()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Move Pac-Man
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        pacman.move(dx, dy)

        # Check for collisions with pellets
        for pellet in pellets[:]:
            if (pacman.x - pellet.x) ** 2 + (pacman.y - pellet.y) ** 2 <= (pacman.radius + pellet.radius) ** 2:
                pellets.remove(pellet)
                score += PELLET_SCORE
                pygame.mixer.Sound.play(pac_man_chomp_sound)

        # Draw the game objects
        window.fill(BLACK)
        pacman.draw()
        for pellet in pellets:
            pellet.draw()
        pygame.display.flip()

        # Check for game over
        if not pellets:
            game_over = True
            game_over_timer = pygame.time.get_ticks()
            pygame.mixer.Sound.play(game_over_sound)

        if game_over and pygame.time.get_ticks() - game_over_timer >= GAME_OVER_DELAY * 1000:
            break

        clock.tick(GAME_SPEED)

    print("Final score:", score)

if __name__ == "__main__":
    game_loop()