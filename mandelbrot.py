import pygame
from pygame import gfxdraw
from collections import defaultdict
from math import floor, ceil, log, log2

MAX_ITER = 80

WIDTH = 1000
HEIGHT = 800

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t 

def mandelbrot(c):    
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER
    
    return n + 1 - log(log2(abs(z)))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Arial', 12)

def draw():
    message1 = font.render(
        f'Pos x: {posX} Pos y: {posY} Zoom: {zoom}', False, (128, 128, 128))
    message_rect1 = message1.get_rect(topleft = (10, 10))
    screen.blit(message1, message_rect1)

    message2 = font.render(
        f'Press R to reset, Z OR X to zoom in and out, arrow keys or mouse click to move', False, (128, 128, 128))
    message_rect2 = message2.get_rect(topleft = (10, 25))
    screen.blit(message2, message_rect2)

    histogram = defaultdict(lambda: 0)
    values = {}
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            c = complex(-posX + (x / WIDTH) * zoom,
                        -posY + (y / HEIGHT) * zoom)
                        
            m = mandelbrot(c)
            
            values[(x, y)] = m
            if m < MAX_ITER:
                histogram[floor(m)] += 1

    total = sum(histogram.values())
    hues = [0]
    h = 0
    for i in range(MAX_ITER):
        if total > 0:
            h += histogram[i] / total
        hues.append(h)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            m = values[(x, y)]
            
            hue = 255 - int(255 * linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1))
            saturation = 255
            value = 255 if m < MAX_ITER else 0

            gfxdraw.pixel(screen, x, y, (hue, saturation, value))
    return True

drawn = False
zoom = 2
posX = 1
posY = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                posX -= .1
            if event.key == pygame.K_RIGHT:
                posX += .1
            if event.key == pygame.K_UP:
                posY -= .1
            if event.key == pygame.K_DOWN:
                posY += .1
            if event.key == pygame.K_z:
                zoom /= 2
            if event.key == pygame.K_x and zoom > .01:
                zoom *= 2
            if event.key == pygame.K_r:
                zoom = 2
                posX = 1
                posY = 1
            screen.fill((0, 0, 0))
            drawn = False

    if drawn == False:
        drawn = draw()

    dispZoom = 1 / zoom
    message1 = font.render(
        f'Pos x: {posX} Pos y: {posY} Zoom: {dispZoom}', False, (128, 128, 128))
    message_rect1 = message1.get_rect(topleft = (10, 10))
    screen.blit(message1, message_rect1)

    message2 = font.render(
        f'Press R to reset, Z OR X to zoom in and out, arrow keys or mouse click to move', False, (128, 128, 128))
    message_rect2 = message2.get_rect(topleft = (10, 25))
    screen.blit(message2, message_rect2)

    pygame.display.update()