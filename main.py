import pygame
import getopt
import sys
from ui import *
from utils import load_data
from astar import *
import time
import tracemalloc

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
    size, boxPos, targetPos, tile = load_data("testcase/test_3.txt")
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
start = Position(boxPos[0], boxPos[1])
goal = Position(targetPos[0], targetPos[1])
map = Map(size, start, goal, tile)
a_start_solver = AStarSolver(map)
current = Block(start, start)

targetX = initX + targetPos[0] * unit
targetY = initY + targetPos[1] * unit

step = 0
isStand = True  # check if block Stand
keypress = ''
isWin = False


def checkOutMap(currentPos1, currentPos2, tile):
    if currentPos1[0] < 0 or currentPos2[0] < 0 or currentPos1[1] < 0 or currentPos2[1] < 0:
        return True
    if currentPos1[0] >= size[1] or currentPos2[0] >= size[1] or currentPos1[1] >= size[0] or currentPos2[1] >= size[0]:
        return True
    if tile[currentPos1[1]][currentPos1[0]] == 0 or tile[currentPos2[1]][currentPos2[0]] == 0:
        return True
    return False


def bfs(currentPos1, currentPos2, tile):
    queue = []
    visit = []
    move = []
    current = (-1, -1)
    visit.append((currentPos1, currentPos2))
    queue.append((currentPos1, currentPos2))
    while len(queue) > 0:
        print('Queue:', queue)
        print('Visit:', visit)
        current = queue.pop(0)  # FIFO
        print('Current: ', current)

        # move 4 direction -> BFS
        # move up down
        pos1_up, pos2_up, pos1_down, pos2_down = 0, 0, 0, 0
        pos1_left, pos2_left, pos1_right, pos2_right = 0, 0, 0, 0
        if currentPos1[1] == currentPos2[1]:  # cùng y --
            if currentPos1[0] == currentPos2[0]:  # 1 block to 2 block
                pos2_up = (currentPos2[0], currentPos2[1] - 1)
                pos1_up = (currentPos1[0], currentPos1[1] - 2)
                pos1_down = (currentPos1[0], currentPos1[1] + 1)
                pos2_down = (currentPos2[0], currentPos2[1] + 2)
            else:
                pos1_up = (currentPos1[0], currentPos1[1] - 1)
                pos2_up = (currentPos2[0], currentPos2[1] - 1)
                pos1_down = (currentPos1[0], currentPos1[1] + 1)
                pos2_down = (currentPos2[0], currentPos2[1] + 1)
        else:  # 2 block to 1 block
            pos1_up = (currentPos1[0], currentPos1[1] - 1)
            pos2_up = (currentPos2[0], currentPos2[1] - 2)
            pos2_down = (currentPos2[0], currentPos2[1] + 1)
            pos1_down = (currentPos1[0], currentPos1[1] + 2)
        # print('pos1_up, pos2_up, pos1_down, pos2_down', pos1_up, pos2_up, pos1_down, pos2_down)

        # move left right
        if currentPos1[0] == currentPos2[0]:
            if currentPos1[1] == currentPos2[1]:
                pos2_left = (currentPos2[0] - 1, currentPos2[1])
                pos1_left = (currentPos2[0] - 2, currentPos1[1])
                pos1_right = (currentPos1[0] + 1, currentPos1[1])
                pos2_right = (currentPos1[0] + 2, currentPos2[1])
            else:
                pos1_left = (currentPos1[0] - 1, currentPos1[1])
                pos2_left = (currentPos2[0] - 1, currentPos2[1])
                pos1_right = (currentPos1[0] + 1, currentPos1[1])
                pos2_right = (currentPos2[0] + 1, currentPos2[1])
        else:
            pos1_left = (currentPos1[0] - 1, currentPos1[1])
            pos2_left = (currentPos1[0] - 1, currentPos2[1])
            pos2_right = (currentPos2[0] + 1, currentPos2[1])
            pos1_right = (currentPos2[0] + 1, currentPos1[1])
        # checkOutmap
            # check visit
            # append to Queue and Visit
        if not checkOutMap(pos1_up, pos2_up, tile):  # continue
            if (pos1_up, pos2_up) not in visit:
                currentPos1 = pos1_up
                currentPos2 = pos2_up
                move.append('U')
                queue.append((pos1_up, pos2_up))
                visit.append((pos1_up, pos2_up))
        if not checkOutMap(pos1_down, pos2_down, tile):  # continue
            if (pos1_down, pos2_down) not in visit:
                currentPos1 = pos1_down
                currentPos2 = pos2_down
                move.append('D')
                queue.append((pos1_down, pos2_down))
                visit.append((pos1_down, pos2_down))
        if not checkOutMap(pos1_left, pos2_left, tile):  # continue
            if (pos1_left, pos2_left) not in visit:
                currentPos1 = pos1_left
                currentPos2 = pos2_left
                move.append('L')
                queue.append((pos1_left, pos2_left))
                visit.append((pos1_left, pos2_left))
        if not checkOutMap(pos1_right, pos2_right, tile):  # continue
            if (pos1_right, pos2_right) not in visit:
                currentPos1 = pos1_right
                currentPos2 = pos2_right
                move.append('R')
                queue.append((pos1_right, pos2_right))
                visit.append((pos1_right, pos2_right))
        print(move)
        print('-------------')
        # checkWin
        if ((targetPos, targetPos) in visit):
            queue.append((targetPos, targetPos))
            print('WIN !!!')
            return True
    return False


tracemalloc.start()
start_time = time.time()
print("Solution by A* algorithm:", a_start_solver.solve(),
      "\nin", time.time() - start_time, "seconds")
print(tracemalloc.get_traced_memory()[1])
tracemalloc.stop()

# Game loop
# if sys.argv[0] == 'BFS'  or sys.argv[0] == 'bfs':
running = True
while running:
    screen.fill((255, 255, 255))  # background

    stepText = my_font.render('{} {} {} {}'.format(
        currentPos1[0], currentPos1[1], currentPos2[0], currentPos2[1]), False, (0, 0, 0))
    screen.blit(stepText, (430, 100))

    # check WIN & LOSE
    if checkOutMap(currentPos1, currentPos2, tile):
        gameStatus = my_font.render('You lose!', True, (255, 0, 0))
        screen.blit(gameStatus, (415, 50))
        # check Win
    elif currentPos1 == targetPos and currentPos2 == targetPos:
        gameStatus = my_font.render('You win!', True, (0, 185, 0))
        screen.blit(gameStatus, (415, 50))

    # if (bfs(currentPos1, currentPos2, tile)):
    #     running = False
    # else:
    #     print('Can\'t solve!')
    #     running = False

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False
        # Move block
        if event.type == pygame.KEYDOWN:
            keypress = event.key
            # Gameplay -> class Move
            # if currentPos1[0] > currentPos2[0]:
            #     currentPos1[0], currentPos2[0] = currentPos2[0], currentPos1[0]
            # if currentPos1[1] > currentPos2[1]:
            #     currentPos1[1], currentPos2[1] = currentPos2[1], currentPos1[1]
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
        # print(currentPos1, currentPos2)
    # if event.key == pygame.K_q: # back step <- history

    # draw map & block
    for i in range(size[0]):
        for j in range(size[1]):
            if tile[i][j] == 1:
                UI.createTile(screen, 'normalTile', initX +
                              int(j)*unit, initY + int(i)*unit)
    UI.createTile(screen, 'targetTile', targetX, targetY)
    UI.createBox(screen, initX +
                 currentPos1[0]*unit, initY + currentPos1[1]*unit)
    UI.createBox(screen, initX +
                 currentPos2[0]*unit, initY + currentPos2[1]*unit)

    # Gameplay.checkWin(blockX, blockY, boxPos)
    pygame.display.update()
