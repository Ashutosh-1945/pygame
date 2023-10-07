import pygame
import random
from PIL import Image
from pygame import mixer
import math

def re():
    image = Image.open('arcade-game.png')
    resized = image.resize((64, 64))
    resized.save('shooter.png')

    image2 = Image.open('alien.png')
    resize2 = image2.resize((64, 64))
    resize2.save('enemy.png')

    image3 = Image.open('back.png')
    resize3 = image3.resize((800,600))
    resize3.save('bk.png')

    image4 = Image.open('b.png')
    resize4 = image4.resize((32,32))
    resize4.save('bullet.png')

re()

# initaloze the pygame
pygame.init()

#back
background = pygame.image.load('bk.png')
screen = pygame.display.set_mode((800, 600))

#?back music
mixer.music.load('backm.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Chicken Invaders")
icon = pygame.image.load('32x32 (1).png')
pygame.display.set_icon(icon)

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# player
playerimg = pygame.image.load('shooter.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# bullet
#ready = not seen
#Fire = fired moving
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
#For different font place it in the file and use it
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score :" +str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text( ):
    over_text = over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(over_text, (200,250))
def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16,y+10) )

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


# game loop to make gaming running until closed
running = True
while running:
    # anything that we want to be continuous in game is placed here
    screen.fill((56, 25, 2))
    #back image
    screen.blit(background,(0,0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
                print("Left key pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = +4
                print("Right key pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('firem.mp3')
                    bullet_sound.play()
                    #Get the current X coordinate of player
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("Key released")

    # always draw player after filling color on screen
    playerX += playerX_change

    #checking boumdaries to retain
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736 and over == False:
        playerX = 736
    player(playerX, playerY)

    #bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY=480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    #enemy move
    for i in range(number_of_enemies):
        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Game over
        if enemyY[i] > 200:
            for j in range(number_of_enemies):
                enemyY[j] = 2000

            playerX = 2000
            over = True
            game_over_text()
            break


        # collide
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision is True:
            collide_sound = mixer.Sound('shotm.mp3')
            collide_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)


        enemy(enemyX[i], enemyY[i], i)

    show_score(textX,textY)

    pygame.display.update()  # always used to update any change
