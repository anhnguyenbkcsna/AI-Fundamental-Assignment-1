import pygame
import sys
from ui import *
from gameplay import *
from utils import load_data

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
try:
    size, boxPos, targetPos, tile = load_data("testcase/test_3.txt")
except ValueError as e:
    print("Error when loading testcase. Default testcase is used.")
    size = (7, 7)  # start from 0
    boxPos = (3, 2)  # start from 1
    targetPos = [6, 6]  # start from 1
    tile = [
        [0, 0, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1],
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

# block1 always left, down and under
block_1x = blockX
block_2x = blockX
block_1y = blockY
block_2y = blockY

targetX = initX + targetPos[0] * unit
targetY = initY + targetPos[1] * unit

step = 0
isStand = True # check if block Stand
keypress = ''
isWin = False

def checkBorder(block_1x, block_1y, block_2x, block_2y, tile):
    return True;

# Game loop
running = True
while running:
    screen.fill((255,255,255)) # background
    # stepText = my_font.render('Move {}'.format(step), False, (0, 0, 0))
    stepText = my_font.render('{} {} {} {}'.format(block_1x, block_2x, block_1y, block_2y), False, (0, 0, 0))
    screen.blit(stepText, (430,100))
    # stepText = my_font.render('{} {} {} {}'.format(block_1x, block_1y, block_2x, block_2y), False, (0, 0, 0))
    # screen.blit(stepText, (430,100))

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False
        # Move block
        if event.type == pygame.KEYDOWN:
            keypress = event.key
            # Gameplay -> class Move
            if block_1x > block_2x:
                (block_1x, block_2x) = (block_2x, block_1x)
            if block_1y > block_2y:
                (block_1y, block_2y) = (block_2y, block_1y)
            if keypress == pygame.K_a or keypress == pygame.K_LEFT:
                if block_1x == block_2x:
                    if block_1y == block_2y:
                        block_2x -= unit
                        block_1x = block_2x - unit
                    else:
                        block_1x -= unit
                        block_2x -= unit
                else:
                    block_1x -= unit
                    block_2x = block_1x
                step += 1
            if keypress == pygame.K_d or keypress == pygame.K_RIGHT:
                if block_1x == block_2x:
                    if block_1y == block_2y:
                        block_1x += unit
                        block_2x = block_1x + unit
                    else:
                        block_1x += unit
                        block_2x += unit
                else:
                    block_2x += unit
                    block_1x = block_2x
                step += 1
            if keypress == pygame.K_w or keypress == pygame.K_UP:
                if block_1y == block_2y:
                    if block_1x == block_2x:
                        block_2y -= unit
                        block_1y = block_2y - unit
                    else:
                        block_1y -= unit
                        block_2y -= unit
                else:
                    block_1y -= unit
                    block_2y = block_1y
                step += 1
            if keypress == pygame.K_s or keypress == pygame.K_DOWN:
                if block_1y == block_2y:
                    if block_1x == block_2x: # stand
                        block_1y += unit
                        block_2y = block_1y + unit
                    else:
                        block_1y += unit
                        block_2y += unit
                else:
                    block_2y += unit
                    block_1y = block_2y
                step += 1
            if keypress == pygame.K_r: # reset round
                blockX = initX + boxPos[0]*unit
                blockY = initY + boxPos[1]*unit
                step = 0
            # if event.key == pygame.K_q: # back step <- history

    # check Win
    if block_1x == targetX and block_2x == targetX and block_1y == targetY and block_2y == targetY:
        isWin = True
    # draw map & block
    for i in range(size[0]):
        for j in range(size[1]):
            if tile[i][j] == 1:
                UI.createTile(screen, 'normalTile', initX + int(i)*unit, initY + int(j)*unit)
    UI.createTile(screen, 'targetTile', targetX, targetY)
    UI.createBox(screen, block_1x, block_1y)
    UI.createBox(screen, block_2x, block_2y)

    # Gameplay.checkWin(blockX, blockY, boxPos)
    pygame.display.update()
