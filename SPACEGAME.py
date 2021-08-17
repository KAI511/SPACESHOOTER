import pygame
import random
import math
from pygame import mixer

# initialize the pygame

pygame.init()

# create a screen

screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load(
    r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\IMAGES\spacebackground.png")

# background sound
mixer.music.load(r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\SOUNDS\bgm.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("space fighter")
icon = pygame.image.load(r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\IMAGES\rocket.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load(r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\IMAGES\spaceship.png")
playerx = 370
playery = 480
playerx_change = 0

# enemy

enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load(r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\IMAGES\alien.png"))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(1)
    enemyy_change.append(40)

# bullet
# Ready - state screen no see
# Fire - bullet is currently moving
bulletimg = pygame.image.load(r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\IMAGES\bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 5  # my bullets are so fats dont know why
bullet_state = "ready"

scorevalue = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textx = 10
texty = 10

# game over font
over_font = pygame.font.Font("freesansbold.ttf", 64)


def showscore(x, y):
    score = font.render("score:" + str(scorevalue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameover_text():
    over = over_font.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(over, (210, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(
        (math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2))
    )
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # rgb values
    screen.fill((123, 24, 150))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key stroked left or right
        if event.type == pygame.KEYDOWN:
            # keystroke is pressed
            if event.key == pygame.K_LEFT:
                playerx_change = -2
            if event.key == pygame.K_RIGHT:
                playerx_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletsound = mixer.Sound(
                        r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\SOUNDS\laser.wav")
                    bulletsound.play()

                    # get x coordinate of spaceship
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif (
            playerx >= 736
    ):  # since the pixel of rocket is 64 bit so as we reduce the entire width negatived the so the spaceship doesnt get out of screen
        playerx = 736

    # enemy movement

    for i in range(num_of_enemies):

        # gameover
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            gameover_text()
            break

        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 1
            enemyy[i] += enemyy_change[i]
        elif (
                enemyx[i] >= 736
        ):  # since the pixel of rocket is 64 bit so as we reduce the entire width negatived the so the spaceship doesnt get out of screen
            enemyx_change[i] = -1
            enemyy[i] += enemyy_change[i]

        # collision
        col = collision(enemyx[i], enemyy[i], bulletx, bullety)
        if col:
            explosionsound = mixer.Sound(
                r"E:\code\teach pygame sdp\GITHUB UPLOAD TOTAL PROGRAM UPLOAD\SOUNDS\explosion.wav")
            explosionsound.play()
            bullety = 480
            bullet_state = "ready"
            scorevalue += 1
            print(scorevalue)
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    showscore(textx, texty)
    pygame.display.update()
