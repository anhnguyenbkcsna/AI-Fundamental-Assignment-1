import pygame
import sys
from ui import *
from gameplay import *

sys.path.insert(0, '/ui.py')

# intialize the pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 48)


#create the screen
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Bloxor")
pygame.display.set_icon(pygame.image.load('./assets/cube64.png'))

# import assets
blockImage = pygame.image.load('./assets/square.png')

# testcase
size = [7,7]        # start from 0
boxPos = [3,2]      # start from 1
targetPos = [6,6]   # start from 1
tile = [
    [0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, -1, 1],
    [0, 0, 1, 0, 1, 1, 1],
]

# Global variable
unit = 60 # change px to square

initX = int(480 - size[0]*60/2)
lieX = 24
blockX = initX + boxPos[0]*unit

initY = int(380 - size[1]*60/2)
lieY = 14
standY = -32
blockY = initY + boxPos[1]*unit

step = 0
isStand = True # check if block Stand
keypress = ''


# def block(x, y, isStand, keypress):
#     # wrong way to lie
#     screen.blit(blockImage, (x, y)) # cube1
#     if isStand == True:
#         screen.blit(blockImage, (x, y + standY)) # cube2
#     else:
#         screen.blit(blockImage, (x+ lieX, y + lieY))

# Game loop
running = True
while running: 
    screen.fill((255,255,255)) # background
    stepText = my_font.render('Step {}'.format(step), False, (0, 0, 0))
    screen.blit(stepText, (430,100))

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False
        # Move block
        if event.type == pygame.KEYDOWN:
            keypress = event.key
            isStand = not isStand
            if keypress == pygame.K_a or keypress == pygame.K_LEFT:
                blockX -= unit
                step += 1
            if keypress == pygame.K_d or keypress == pygame.K_RIGHT:
                blockX += unit
                step += 1
            if keypress == pygame.K_w or keypress == pygame.K_UP:
                blockY -= unit
                step += 1
            if keypress == pygame.K_s or keypress == pygame.K_DOWN:
                blockY += unit
                step += 1
            if keypress == pygame.K_r: # reset round
                blockX = initX + boxPos[0]*unit
                blockY = initY + boxPos[1]*unit
                step = 0
            # if event.key == pygame.K_q: # back step <- history
        
        # boundary? 

    # draw map & block
    for i in range(size[0]):
        for j in range(size[1]):
            if tile[i][j] == 1:
                UI.createTile(screen, 'normalTile', initX + int(i)*unit, initY + int(j)*unit)
            if tile[i][j] == -1:
                UI.createTile(screen, 'targetTile', initX + int(i)*unit, initY + int(j)*unit)
    UI.createBox(screen, blockX, blockY)
    
    Gameplay.checkWin(blockX, blockY, boxPos)
    pygame.display.update()