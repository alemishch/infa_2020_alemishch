import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

yellow = (255, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

rect(screen, white, (0, 0, 400, 400), 0)
circle(screen, yellow, (200, 200), 100)
circle(screen, red, (170, 190), 15)
circle(screen, red, (235, 180), 20)

circle(screen, black, (170, 190), 5)
circle(screen, black, (235, 180), 7)

rect(screen, black, (165, 240, 70, 20))
polygon(screen, black, ((145, 150), (195, 170), (195, 185), (145, 165)))
polygon(screen, black, ((205, 160), (255, 145), (265, 155), (210, 170)))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
#11 12