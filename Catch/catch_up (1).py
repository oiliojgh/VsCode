from pygame import *

window = display.set_mode((800, 600))
display.set_caption("Catch")
background = transform.scale(image.load("background.jpg"), (800, 600))

sprite1 = transform.scale(image.load("sprite1.png"), (100, 100))
sprite1 = transform.scale(image.load("sprite2.png"), (100, 100))


x1 = 100
y1 = 300

clock = time.Clock()
FPS = 60

game = True
while game:
    window.blit(background, (0, 0))
    window.blit(sprite1, (x1, x1))

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)