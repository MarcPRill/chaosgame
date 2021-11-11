import pygame
import random
from pygame import gfxdraw
from pygame.constants import KEYDOWN

i = 0
border = 50
zoom = 2

h = 0
w = 0

posX = 0
posY = 0

pygame.init()
screen = pygame.display.set_mode((1000, 800))
font = pygame.font.SysFont('Arial', 12)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                posX -= 100
            if event.key == pygame.K_RIGHT:
                posX += 100
            if event.key == pygame.K_UP:
                posY -= 100
            if event.key == pygame.K_DOWN:
                posY += 100
            if event.key == pygame.K_z:
                posX -= 125 * zoom
                zoom *= 2
            if event.key == pygame.K_x and zoom > 1:
                zoom /= 2
                posX += 125 * zoom
            if event.key == pygame.K_r:
                zoom = 2
                posX = 0
                posY = 0
            screen.fill((0, 0, 0))
            i = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            posX -= (pygame.mouse.get_pos()[0] / 2) - 250
            posY -= (pygame.mouse.get_pos()[1] / 2) - 200
            screen.fill((0, 0, 0))
            i = 0

    r = random.randint(0, 2)
    if r == 1:  # left
        h = (h + (400 * zoom)) / 2 - border + posY
        w = (w + 0) / 2 + border + posX
    elif r == 2:  # right
        h = (h + (400 * zoom)) / 2 - border + posY
        w = (w + (500 * zoom)) / 2 - border + posX
    else:  # up
        h = (h + 0) / 2 + border + posY
        w = (w + (250 * zoom)) / 2 + posX

    if i > 10 and h > 0 and h < 800 and w > 0 and w < 1000:
        gfxdraw.rectangle(screen, (w, h, 0, 0), (255, 255, 255))

    i += 1
    if i % 100000 == 0:
        message1 = font.render(
            f'Pos x: {posX} Pos y: {posY} Zoom: {zoom}', False, (128, 128, 128))
        message_rect1 = message1.get_rect(topleft = (10, 10))
        screen.blit(message1, message_rect1)

        message2 = font.render(
            f'Press R to reset, Z OR X to zoom in and out, arrow keys or mouse click to move', False, (128, 128, 128))
        message_rect2 = message2.get_rect(topleft = (10, 25))
        screen.blit(message2, message_rect2)

        pygame.display.update()
