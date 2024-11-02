from pygame import *

window = display.set_mode((800, 600))
display.set_caption("Catch")
background = transform.scale(image.load("background.jpg"), (800, 600))

sprite1_r = transform.scale(image.load("sprite1.png"), (100, 100))
sprite1_l = transform.flip(sprite1_r, True, False)
sprite2_r = transform.scale(image.load("sprite2.png"), (100, 100))
sprite2_l = transform.flip(sprite2_r, True, False)

current_sprite1 = sprite1_r
current_sprite2 = sprite2_r



x1 = 100
y1 = 300

x2 = 300
y2 = 300

clock = time.Clock()
FPS = 60

game = True
while game:
    window.blit(background, (0, 0))
    window.blit(current_sprite1, (x1, y1))
    window.blit(current_sprite2, (x2, y2))

    for e in event.get():
        if e.type == QUIT:
            game = False

    keys_pressed = key.get_pressed()

    if keys_pressed[K_UP] and y1 > 5:
        y1 -= 10
    if keys_pressed[K_DOWN] and y1 < 600 - 105:
        y1 += 10
    if keys_pressed[K_LEFT] and x1 > 5:
        x1 -= 10
        current_sprite1 = sprite1_l
    if keys_pressed[K_RIGHT] and x1 < 800 - 105:
        x1 += 10
        current_sprite1 = sprite1_r
    if keys_pressed[K_w] and y2 > 5:
        y2 -= 10
    if keys_pressed[K_s] and y2 < 600 - 105:
        y2 += 10
    if keys_pressed[K_a] and x2 > 5:
        x2 -= 10
        current_sprite2 = sprite2_l
    if keys_pressed[K_d] and x2 < 800 - 105:
        x2 += 10
        current_sprite2 = sprite2_r
        



    

    display.update()
    clock.tick(FPS)