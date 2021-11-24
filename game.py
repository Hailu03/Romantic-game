import pygame
import random
import math
from pygame import mixer

pygame.init()

FPS = 60
fpsclock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('background.png')

# you
haiImg = []
haiX = []
haiY = []
haiX_change = []
haiY_change = []
num_of_hai = 5

for i in range(num_of_hai):
    haiImg.append(pygame.image.load('hai.png'))
    haiX.append(random.randint(0,735))
    haiY.append(random.randint(20,150))
    haiX_change.append(0.2)
    haiY_change.append(20)

    def hai(x,y,i):
        screen.blit(haiImg[i],(x,y))

# your girl friend
nganImg = pygame.image.load('ngan.png')
nganX = 380
nganY = 500
nganX_change = 0
nganY_change = 0

def ngan(x,y):
    screen.blit(nganImg,(x,y))

# heart
heartImg = pygame.image.load('heart.png')
heartX = 0
heartY = nganY
heartX_change = 0
heartY_change = 0.4

heart_state = "ready"

def heart(x,y):
    global heart_state
    heart_state = "fire"
    screen.blit(heartImg,(x+16,y+10))

# icon and title
title = pygame.display.set_caption("AnhYêuEm")
icon = pygame.image.load('heart.png')
pygame.display.set_icon(icon)

# check colision
def iscollision(haiX,haiY,heartX,heartY):
    distance = math.sqrt(math.pow(haiX - heartX,2)+math.pow(haiY - heartY,2))

    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Yêu Anh x " + str(score_value),True, (150,150,255))
    screen.blit(score,(x,y))

# Game over
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("You lost but I still love u" ,True, (150,150,255))
    screen.blit(over_text,(30,250))

# sound and music
mixer.music.load("cauhon.wav")
mixer.music.play(-1)

running = True
while running:

    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                nganX_change = 1
            if event.key == pygame.K_LEFT:
                nganX_change = -1
            if event.key == pygame.K_UP:
                nganY_change = -1
            if event.key == pygame.K_DOWN:
                nganY_change = 1
            if event.key == pygame.K_SPACE:
                if heart_state == "ready":
                    heartX = nganX
                    heartY = nganY
                    heart(heartX,heartY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                nganX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                nganY_change = 0

    ngan(nganX,nganY)
    nganX += nganX_change
    nganY += nganY_change

    if nganX <=0:
        nganX = 0 
    elif nganX >=736:
        nganX = 736

    if nganY <= 400: 
        nganY = 400
    elif nganY >=530:
        nganY = 529

    for i in range(num_of_hai):
        # game over
        if haiY[i] > 200:
            for j in range(num_of_hai):
                haiY[j] =2000
            game_over_text()
            break

        hai(haiX[i],haiY[i],i)

        if haiX[i] <= 0:
            haiX_change[i] = 0.2
            haiY[i] += haiY_change[i]
        if haiX[i] >= 736:
            haiX_change[i] = -0.2
            haiY[i] += haiY_change[i]

        haiX[i] += haiX_change[i]
           
        collision = iscollision(haiX[i],haiY[i],heartX,heartY)
        if collision:
            heart_state = "ready"
            haiY[i] = random.randint(50,150)
            haiX[i] = random.randint(0,735)
            score_value += 1
            explosion_sound = mixer.Sound('tick.wav')
            explosion_sound.play()

    if heartY <= 0:
        heartY = nganY
        heart_state ="ready" 
    if heart_state == "fire":
        heartY -= heartY_change
        heart(heartX,heartY)

    show_score(textX,textY)
    fpsclock.tick()
    pygame.display.flip()
