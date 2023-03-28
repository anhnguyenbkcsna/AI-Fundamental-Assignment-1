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


# create the screen
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Bloxor")
pygame.display.set_icon(pygame.image.load('./assets/cube64.png'))

# import assets
blockImage = pygame.image.load('./assets/square.png')

# testcase
try:
    size, boxPos, targetPos, tile = load_data("testcase/test_1.txt")
except ValueError as e:
    print("Error when loading testcase. Default testcase is used.")
    size = (7, 7)  # start from 0
    boxPos = (3, 2)  # start from 1
    targetPos = (6, 6)  # start from 1
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
unit = 60  # change px to square

initX = int(480 - size[0]*60/2)
lieX = 24
blockX = initX + boxPos[0]*unit

initY = int(380 - size[1]*60/2)
lieY = 14
standY = -32
blockY = initY + boxPos[1]*unit

# block1 always left, down and under
currentPos1 = boxPos
currentPos2 = boxPos

targetX = initX + targetPos[0] * unit
targetY = initY + targetPos[1] * unit

step = 0
isStand = True  # check if block Stand
keypress = ''
isWin = False



def checkOutMap(currentPos1, currentPos2, tile):
    if currentPos1[0] < 0 or currentPos2[0] < 0 or currentPos1[1] < 0 or currentPos2[1] < 0:
        return True
    if currentPos1[0] >= size[0] or currentPos2[0] >= size[0] or currentPos1[1] >= size[1] or currentPos2[1] >= size[1]:
        return True
    if tile[currentPos1[0]][currentPos1[1]] == 0 or tile[currentPos2[0]][currentPos2[1]] == 0:
        return True
    return False


def bfs(blockX, blockY, targetX, targetY, tile):
    queue = []
    visit = []
    queue.append((blockX, blockY, blockX, blockY))
    while len(queue) > 0:
        print(queue, visit)
        current = queue.pop(0) # FIFO
        if current[0] == targetX and current [2] == targetX and current[1] == targetY and current[3] == targetY:
            return current
        currentPos1[0] = current[0]
        currentPos1[1] = current[1]
        currentPos2[0] = current[2]
        currentPos2[1] = current[3]
        
        # move 4 direction -> BFS
            # move up
        if currentPos1[1] == currentPos2[1]:
            if currentPos1[0] == currentPos2[0]:
                currentPos2[1] -= 1
                currentPos1[1] = currentPos2[1] - 1
            else:
                currentPos1[1] -= 1
                currentPos2[1] -= 1
        else:
            currentPos1[1] -= 1
            currentPos2[1] = currentPos1[1]
        # check border
        if (currentPos1, currentPos2) not in visit:
            visit.append((currentPos1, currentPos2))
            queue.append((currentPos1, currentPos2))
            # move down
        if currentPos1[1] == currentPos2[1]:
            if currentPos1[0] == currentPos2[0]: # stand
                currentPos1[1] += unit
                currentPos2[1] = currentPos1[1] + unit
            else:
                currentPos1[1] += unit
                currentPos2[1] += unit
        else:
            currentPos2[1] += unit
            currentPos1[1] = currentPos2[1]
        if (currentPos1, currentPos2) not in visit:
            visit.append((currentPos1, currentPos2))
            queue.append((currentPos1, currentPos2))
            # move left
        if currentPos1[0] == currentPos2[0]:
            if currentPos1[1] == currentPos2[1]:
                currentPos2[0] -= unit
                currentPos1[0] = currentPos2[0] - unit
                currentPos2 = (currentPos2[0] - 1, currentPos2[1])
                currentPos1 = (currentPos2[0] - 1, currentPos1[1])
            else:
                currentPos1[0] -= unit
                currentPos2[0] -= unit
                currentPos1 = (currentPos1[0] - 1, currentPos1[1])
                currentPos2 = (currentPos2[0] - 1, currentPos2[1])
        else:
            currentPos1[0] -= unit
            currentPos2[0] = currentPos1[0]
            currentPos1 = (currentPos1[0] - 1, currentPos1[1])
            currentPos2 = (currentPos1[0], currentPos2[1])
        if checkOutMap(currentPos1, currentPos2, tile):
            if (currentPos1[0], currentPos1[1], currentPos2[0], currentPos2[1]) not in visit:
                visit.append((currentPos1[0], currentPos1[1], currentPos2[0], currentPos2[1]))
                queue.append((currentPos1[0], currentPos1[1], currentPos2[0], currentPos2[1])) 
            # move right
        if currentPos1[0] == currentPos2[0]:
            if currentPos1[1] == currentPos2[1]:
                currentPos1[0] += unit
                currentPos2[0] = currentPos1[0] + unit
            else:
                currentPos1[0] += unit
                currentPos2[0] += unit
        else:
            currentPos2[0] += unit
            currentPos1[0] = currentPos2[0]
        if (currentPos1, currentPos2) not in visit:
            visit.append((currentPos1, currentPos2))
            queue.append((currentPos1, currentPos2))
    return None

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # background

    stepText = my_font.render('{} {} {} {}'.format(currentPos1[0], currentPos2[0], currentPos1[1], currentPos2[1]), False, (0, 0, 0))
    screen.blit(stepText, (430, 100))
    
    # check WIN & LOSE
    if checkOutMap(currentPos1, currentPos2, tile):
        gameStatus = my_font.render('You lose!', True, (255, 0, 0))
        screen.blit(gameStatus, (415, 50))
            # check Win
    elif currentPos1 == targetPos and currentPos2 == targetPos:
        gameStatus = my_font.render('You win!', True, (0, 185, 0))
        screen.blit(gameStatus, (415, 50))
    
    # bfs(blockX, blockY, blockX, blockY, tile)
    
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False
        # Move block
        if event.type == pygame.KEYDOWN:
            keypress = event.key
            # Gameplay -> class Move
            if currentPos1[0] > currentPos2[0]:
                currentPos1[0], currentPos2[0] = currentPos2[0], currentPos1[0]
            if currentPos1[1] > currentPos2[1]:
                currentPos1[1], currentPos2[1] = currentPos2[1], currentPos1[1]
            if keypress == pygame.K_a or keypress == pygame.K_LEFT:
                if currentPos1[0] == currentPos2[0]:
                    if currentPos1[1] == currentPos2[1]:
                        currentPos2 = (currentPos2[0] - 1, currentPos2[1])
                        currentPos1 = (currentPos2[0] - 1, currentPos1[1])
                    else:
                        currentPos1 = (currentPos1[0] - 1, currentPos1[1])
                        currentPos2 = (currentPos2[0] - 1, currentPos2[1])
                else:
                    currentPos1 = (currentPos1[0] - 1, currentPos1[1])
                    currentPos2 = (currentPos1[0], currentPos2[1])
                step += 1
            if keypress == pygame.K_d or keypress == pygame.K_RIGHT:
                if currentPos1[0] == currentPos2[0]:
                    if currentPos1[1] == currentPos2[1]:
                        currentPos1 = (currentPos1[0] + 1, currentPos1[1])
                        currentPos2 = (currentPos1[0] + 1, currentPos2[1])
                    else:
                        currentPos1 = (currentPos1[0] + 1, currentPos1[1])
                        currentPos2 = (currentPos2[0] + 1, currentPos2[1])
                else:
                    currentPos2 = (currentPos2[0] + 1, currentPos2[1])
                    currentPos1 = (currentPos2[0], currentPos1[1])
                step += 1
            if keypress == pygame.K_w or keypress == pygame.K_UP:
                if currentPos1[1] == currentPos2[1]:
                    if currentPos1[0] == currentPos2[0]:
                        currentPos2 = (currentPos2[0], currentPos2[1] - 1)
                        currentPos1 = (currentPos1[0], currentPos2[1] - 1)
                    else:
                        currentPos1 = (currentPos1[0], currentPos1[1] - 1)
                        currentPos2 = (currentPos2[0], currentPos2[1] - 1)
                else:
                    currentPos1 = (currentPos1[0], currentPos1[1] - 1)
                    currentPos2 = (currentPos2[0], currentPos1[1])
                step += 1
            if keypress == pygame.K_s or keypress == pygame.K_DOWN:
                if currentPos1[1] == currentPos2[1]:
                    if currentPos1[0] == currentPos2[0]:  # stand
                        currentPos1 = (currentPos1[0], currentPos1[1] + 1)
                        currentPos2 = (currentPos2[0], currentPos1[1] + 1)
                    else:
                        currentPos1 = (currentPos1[0], currentPos1[1] + 1)
                        currentPos2 = (currentPos2[0], currentPos2[1] + 1)
                else:
                    currentPos2 = (currentPos2[0], currentPos2[1] + 1)
                    currentPos1 = (currentPos1[0], currentPos2[1])
                step += 1
            if keypress == pygame.K_r:  # reset round
                blockX = initX + boxPos[0]*unit
                blockY = initY + boxPos[1]*unit
                currentPos1 = boxPos
                currentPos2 = boxPos
                step = 0
        # if event.key == pygame.K_q: # back step <- history


    # draw map & block
    for i in range(size[0]):
        for j in range(size[1]):
            if tile[i][j] == 1:
                UI.createTile(screen, 'normalTile', initX +
                              int(i)*unit, initY + int(j)*unit)
    UI.createTile(screen, 'targetTile', targetX, targetY)
    UI.createBox(screen, initX + currentPos1[0]*unit, initY + currentPos1[1]*unit)
    UI.createBox(screen, initX + currentPos2[0]*unit, initY + currentPos2[1]*unit)

    # Gameplay.checkWin(blockX, blockY, boxPos)
    pygame.display.update()
