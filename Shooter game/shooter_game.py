#importing module
import random
from pygame import *

SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Class-----------------------------------------------------------------------------------------------
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, Sx, Sy):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (Sx, Sy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        elif keys[K_d]:
            self.rect.x += self.speed
        elif keys[K_w]:
            self.rect.y -= self.speed
        elif keys[K_s]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def shoot(self):
        bullet = Bullet(('bullet.png'), self.rect.centerx - 9, self.rect.top, 15, 20, 15)
        bullets.add(bullet) 

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-SCREEN_HEIGHT, 0)
            self.rect.x = random.randint(0, SCREEN_WIDTH)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Particle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-SCREEN_HEIGHT, 0)  # Start off-screen
        self.size = random.randint(1, 3)
        self.speed = random.uniform(1, 5)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-20, 0)
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, window):
        draw.circle(window, WHITE, (self.x, self.y), self.size)

#other functions--------------------------------------------------------------------------------
window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
# window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN | SCALED, vsync=1)
display.set_caption('Space Invaders')

    # Generate a list of particles
particles = [Particle() for _ in range(100)]

player = Player(('rocket.png'), 400, 300, 5, 50, 60)

enemies = sprite.Group()
    # Create enemies
for i in range(6):  # You can change the number of enemies
    enemy = Enemy(('ufo.png'), random.randint(0, SCREEN_WIDTH), random.randint(-SCREEN_HEIGHT, 0), random.randint(2, 5), 50, 50)
    enemies.add(enemy)


ships = sprite.Group()
    # Create ships
for i in range(2):  # You can change the number of ships
    ship = Enemy(('ship.png'), random.randint(0, SCREEN_WIDTH), random.randint(-200, -100), random.randint(2, 5), 50, 50)
    ships.add(ship)

bullets = sprite.Group()


clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()

#update, reset stuff----------------------------------------------------------------
game = True
finish = False

shooting = 0


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif (e.type == MOUSEBUTTONDOWN and e.button == 1) or (e.type == KEYDOWN and e.key == K_SPACE):
            if shooting == 0:
                player.shoot()
                shooting = 1
  
    if shooting > 0:
        shooting -= 1


    if not finish:
        window.fill(BLACK)

        # Update and draw all particles
        for particle in particles:
            particle.update()
            particle.draw(window)

        player.update()
        player.reset()

        
        # Update and draw enemies in the game loop
        enemies.update()
        enemies.draw(window)

        ships.update()
        ships.draw(window)

        bullets.update()
        bullets.draw(window)

        display.update()
        clock.tick(FPS)