import pygame
from pygame.draw import *

pygame.init()

pi = 3.14159265359
FPS = 30
screen = pygame.display.set_mode((600, 900))

yellow = (255, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
whitt = (255, 237, 237)
brown = (150, 75, 0)

rect(screen, white, (0, 0, 600, 900))
rect(screen, whitt, (0, 0, 600, 400))

circle(screen, white, (200, 500), 160)
arc(screen, black, (40, 340, 320, 320), 0, pi, 3)

ellipse(screen, brown, (400, 500, 100, 200), 0)
rect(screen, white, (350, 610, 200, 200), 0)
surface = pygame.Surface((320, 240))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()