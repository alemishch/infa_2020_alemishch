import pygame
import random
pygame.init()

pi = 3.14159265359
srt2=1.41421356237
FPS = 30
screen = pygame.display.set_mode((600, 900))

#color sets

yellow = (255, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
whitt = (255, 237, 237)
brown = (150, 75, 0)
gray = (211,211,211)
fish = (20,255,210)

pygame.draw.rect(screen, white, (0, 0, 600, 900))
pygame.draw.rect(screen, whitt, (0, 0, 600, 400))

#drawing iglu
#x, y - coordinates of top left corner, r - radius
def iglu(x, y, r):
    iglu=pygame.Surface((2*r, r), pygame.SRCALPHA, 32)
    iglu=iglu.convert_alpha()
    pygame.draw.circle(iglu, gray, (r, r), r)
    pygame.draw.arc(iglu, black, (0, 0, 2*r, 2*r), 0, pi, 3)
    pygame.draw.line(iglu, black, (0, r-2), (2*r, r-2), 2)
    pygame.draw.line(iglu, black, (r-r/(srt2), r/(2*srt2)), (r+r/(srt2), r/(2*srt2)), 2)
    pygame.draw.line(iglu, black, (r-r/(0.77*srt2), r/(srt2)), (r+r/(0.77*srt2), r/(srt2)), 2)
    yy = [r, r/srt2, r/(2*srt2)]
    pygame.draw.line(iglu, black, (r, 0), (r, yy[2]))
    for i in range(1, 3):
        delta = random.randint(int(-r/7), int(r/7))
        xx = range(int(r/2), 4*int((r**2-yy[i]**2)**0.5), int(r/3))
        for j in range(0, len(xx)):
            pygame.draw.line(iglu, black, (xx[j]+delta, yy[i]), (xx[j]+delta, yy[i-1]))
    screen.blit(iglu, (x, y))
    

def ellipse(sur, x, y, width, height, color, angle):
    ell=pygame.Surface((width, height), pygame.SRCALPHA, 32)
    ell = ell.convert_alpha()
    pygame.draw.ellipse(ell, color, (0, 0, width, height))
    ell = pygame.transform.rotate(ell, angle)
    sur.blit(ell, (x, y))
    
def cat(x, y, w, color, fish):
    h = int(w / 3)
    cat=pygame.Surface((w, h+30), pygame.SRCALPHA, 32)
    cat = cat.convert_alpha()
    ellipse(cat, int(w/7), int(h/2), int(w/1.5), int(h/2), color, 0)
    ellipse(cat, int(5*w/7), int(h/4), int(w/4), int(h/5), color, 30)
    ellipse(cat, int(4*w/7), int(h/2), int(w/3), int(h/5), color, -45)
    ellipse(cat, int(6*w/14), int(6*h/12), int(w/3), int(h/5), color, -40)
    ellipse(cat, int(3*w/14), int(7*h/8), int(w/5), int(h/5), color, 30)
    ellipse(cat, int(1*w/14), int(13*h/16), int(w/5), int(h/5), color, 30)
    ellipse(cat, int(w/11), int(6*h/20), int(21*w/100), int(15*w/100), color, 0)
    ellipse(cat, int(2.8*w/32), int(6.6*h/15), int(w/6), int(h/6), fish, -30)
    pygame.draw.circle(cat, black, (int(15*w/80), int(12*h/24)), int(w/60))
    pygame.draw.polygon(cat, fish, [(int(w/5), int(8*h/12)), (int(11*w/40), int(8*h/12)), (int(5*w/20), int(10*h/12))], 0)
    pygame.draw.circle(cat, white, (int(5*w/40), int(13*h/24)), int(w/90))
    pygame.draw.circle(cat, white, (int(6*w/40), int(10*h/24)), int(w/42))
    pygame.draw.circle(cat, white, (int(9*w/40), int(10*h/24)), int(w/42))
    pygame.draw.circle(cat, black, (int(9*w/40), int(10*h/24)), int(w/80))
    pygame.draw.circle(cat, black, (int(6*w/40), int(10*h/24)), int(w/80))
    pygame.draw.polygon(cat, color, ((int(4*w/40), int(10*h/24)), (int(5*w/40), int(5*h/24)), (int(7*w/40), int(7*h/24))))
    pygame.draw.polygon(cat, color, ((int(8*w/40), int(7*h/24)), (int(10*w/40), int(5*h/24)), (int(11*w/40), int(10*h/24))))
    pygame.draw.polygon(cat, white, ((int(6*w/40), int(13*h/24)), (int(13*w/80), int(14*h/24)), (int(7*w/40), int(13*h/24))))
    screen.blit(cat, (x, y))
    
def man(color, x, y, w):
    h=int(2*w)
    man=pygame.Surface((w, h), pygame.SRCALPHA, 32)
    man=man.convert_alpha()
    pygame.draw.ellipse(man, color, (int(2*w/5), int(h/5), int(w/5), int(h/8)), 0)
    pygame.draw.ellipse(man, color, (438, 459, 60, 50), 0)
    pygame.draw.rect(man, white, (350, 610, 200, 200), 0)
    screen.blit(man, (x, y))

man(brown, 420, 490, 100)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()