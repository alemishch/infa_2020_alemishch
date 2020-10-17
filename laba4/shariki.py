import pygame
from random import randint as rand
import random
pygame.init()

'''Needed to work with text'''
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

name = input("Enter your name, please\n")

X=1000
Y=700
existance = 1
FPS = 30
timer = 60. #game duration
time = 0. #current playtime
score = 0.
screen = pygame.display.set_mode((X, Y))


'''generates a random colour'''
def color():
    clr = []
    for i in range(3):
        clr.append(rand(0, 253))
    return clr

#some colors
black = (0, 0, 0)
white = (255, 255, 255)


old = pygame.image.load('oldy.png')


ox = rand(0, X - 50)
oy = rand(0, Y-50)
status = 0
ovx = rand(-36, 36)
ovy = (36**2 - ovx**2)**0.5 * random.choice((-1, 1))
ptime = 0.
def Old():
    global ox, oy, status, ovx, ovy, ptime, existance
    if existance:
        if status == 0:
            ovx = rand(-36, 36)
            ovy = (36**2 - ovx**2)**0.5 * random.choice([-1, 1])
            status = 1
        if time - ptime >= 2.:
            status = 0
            ptime = time
        ox += int(ovx / (FPS / 10))
        oy += int(ovy / (FPS / 10))
        if ox <= 0 or ox + 50 >= X:
            ovx *= -1
        if oy <= 0 or oy + 50 >= Y:
            ovy *= -1
        screen.blit(old, (ox, oy))
    

'''creates a new ball with random cordinates x, y and speed vx, vy'''
def new_ball():
    global x, y, r, vx, vy, colour
    r = rand(10, 100)
    x = rand(r + 1, X - r - 1)
    y = rand(r + 1, Y - r - 1)
    vx = rand(-10, 10)
    vy = rand(-10, 10)
    colour = color()
    pygame.draw.circle(screen, colour, (x, y), r)
    

'''draws a ball from list of balls, which is initialized later'''
def ball():
    pygame.draw.circle(screen, balls[i][5], (balls[i][0], balls[i][1]), \
    balls[i][2])
    

'''checks if we hit a target, modifies time and score, score depends on 
   target's speed and size'''
def click(event):
    global time, score, existance, ox, oy
    res = 0
    for i in range(8):
        if ((event.pos[0] - balls[i][0])**2 + (event.pos[1] - 
        balls[i][1])**2) <= balls[i][2]**2:
            score += (balls[i][3]**2 + balls[i][4]**2) / balls[i][2]*10
            balls.pop(i)
            new_ball()
            balls.append(tuple((x, y, r, vx, vy, colour)))
            res +=1
    if ((ox+25-event.pos[0])**2+(oy+25-event.pos[1])**2)**0.5<=25:
        score += 20
        res = 1
        existance = 0
    if res == 0:
        time += 5
    else:
        time -= 4
        
#list of balls     
balls = []


#filling a list with tuples that contain info about each ball
for i in range(8):
    new_ball()
    balls.append(tuple((x, y, r, vx, vy, colour)))
    

def moveBall():
    temp = list(balls[i])
    temp[0] += int(temp[3] * FPS / 15)
    temp[1] += int(temp[4] * FPS / 15)
    if temp[0] + temp[2] > X or temp[0] - temp[2] < 0:
        temp[3] *= -1
    if temp[1] + temp[2] > Y or temp[1] - temp[2] < 0:
        temp[4] *= -1
    balls[i] = tuple(temp)
    ball()


def displayInfo():
    textsurface = myfont.render('Time: ' + str(int(time))
    , False, black) 
    screen.blit(textsurface, (200, 50))
    textsurface = myfont.render('Score: ' + str(int(score))
    , False, black)
    screen.blit(textsurface, (500, 50))


def displayScore():
    textsurface = myfont.render('You lost. Your score is ' + 
    str(int(score)), False, black)
    screen.blit(textsurface,(200,300))

def writeScore():
    with open('test.txt', 'a') as myfile:
        myfile.write(str(name) + '   ' + str(int(score)) + "\n")


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    if time <= timer:
        time += 1/FPS
        for i in range(8):
            moveBall()
        Old()
        displayInfo()
    else:
        displayScore()
    pygame.display.update()
    screen.fill(white)
writeScore()
    
pygame.quit()
    