from pygame import *

S_Width = 700
S_Height = 500

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self, walls):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
            if sprite.spritecollideany(self, walls):
                self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.image = transform.scale(image.load("hero_flip.png"), (65, 65))
            self.rect.x -= self.speed
            if sprite.spritecollideany(self, walls):
                self.rect.x += self.speed
        if keys[K_d] and self.rect.x < S_Width -80:
            self.image = transform.scale(image.load("hero.png"), (65, 65))
            self.rect.x += self.speed
            if sprite.spritecollideany(self, walls):
                self.rect.x -= self.speed            
        if keys[K_s] and self.rect.y < S_Height -80:
            self.rect.y += self.speed
            if sprite.spritecollideany(self, walls):
                self.rect.y -= self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, distance, direction):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.distance = distance
        self.direction = direction
        self.original_x = player_x
        self.original_y = player_y

    def update(self):
        if self.direction == 'left' or self.direction == 'right':
            if self.rect.x <= self.original_x:
                self.direction = 'right'
            elif self.rect.x >= self.original_x + self.distance:
                self.direction = 'left'
            if self.direction == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        elif self.direction == 'up' or self.direction == 'down':
            if self.rect.y <= self.original_y:
                self.direction = 'down'
            elif self.rect.y >= self.original_y + self.distance:
                self.direction = 'up'
            if self.direction == 'up':
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_r,color_g, color_b, wall_x , wall_y , wall_width, wall_height):
        super().__init__()
        self.color_r = color_r        
        self.color_g = color_g        
        self.color_b = color_b
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_r, self.color_g, self.color_b))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


window = display.set_mode((S_Width, S_Height))
display.set_caption("Maze")
background = transform.scale(image.load("background.png"), (S_Width, S_Height))

player = Player("hero.png", 5, 422, 4)
enemy1 = Enemy("cyborg.png", 470, 100, 3, 149, "right")
enemy2 = Enemy("cyborg.png", 470, 100, 3, 149, "up")
treasure = GameSprite("treasure.png", 500, 300, 0)

walls = [
    Wall(154, 205, 50, 100, 20, 450, 10),
    Wall(154, 205, 50, 100, 480, 350, 10),
    Wall(154, 205, 50, 100, 20 , 10, 380),
    Wall(154, 205, 50, 450, 110, 10, 380),
    Wall(154, 205, 50, 230, 110, 10, 380),
    Wall(154, 205, 50, 350, 20, 10, 380),
]


font.init()
font = font.Font(None, 70)

game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("music.mp3")
mixer.music.play()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))

        player.update(walls)
        enemy1.update()
        enemy2.update()

        player.reset()
        enemy1.reset()
        enemy2.reset()
        treasure.reset()
    
        for wall in walls:
            wall.draw_wall() 

        if sprite.collide_rect(player, enemy1) or sprite.collide_rect(player, enemy2):
            finish = True
            lose = font.render("You Lose!", True, (180, 0, 0))
            window.blit(lose, (S_Width // 2 - lose.get_width() // 2, S_Height // 2 - lose.get_height() // 2)) 

        if sprite.collide_rect(player, treasure):
            finish = True
            win = font.render("You Win!", True, (0, 180, 0))
            window.blit(win, (S_Width // 2 - win.get_width() // 2, S_Height // 2 - win.get_height() // 2))

    display.update()
    clock.tick(FPS)




    

