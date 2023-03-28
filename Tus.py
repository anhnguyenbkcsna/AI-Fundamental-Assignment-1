import pygame
import subprocess
import sys
import os
from ui import *
from gameplay import *
from utils import load_data
from button import *
from astar import *
import time
import tracemalloc

# intia pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 48)

# create screen
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Bloxor")
pygame.display.set_icon(pygame.image.load('./assets/cube64.png'))

# import assets
blockImage = pygame.image.load('./assets/square.png')
BG = pygame.image.load("img/bg.jpg")
unit = 60


class Map:
    def __init__(self, file_path):
        try:
            size, boxPos, targetPos, tile = load_data(file_path)
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
        # change px to square

        initX = int(480 - size[0]*60/2)
        lieX = 24
        initY = int(380 - size[1]*60/2)
        lieY = 14
        standY = -32
        self.blockX = initX + boxPos[0]*unit
        self.blockY = initY + boxPos[1]*unit
        self.initX = initX
        self.initY = initY
        self.unit = unit
        self.boxPos = boxPos
        self.targetPos = targetPos
        # block1 always left, down and under
        self.block_1x = self.blockX
        self.block_2x = self.blockX
        self.block_1y = self.blockY
        self.block_2y = self.blockY

        self.targetX = initX + targetPos[0] * unit
        self.targetY = initY + targetPos[1] * unit

        self.step = 0
        self.isStand = True  # check if block Stand
        self.keypress = ''
        self.isWin = False

        self.size = size
        self.tile = tile
        self.rendered = False
# Define the function for rendering the map


def render_map(screen, self):
    for i in range(self.size[0]):
        for j in range(self.size[1]):
            if self.tile[i][j] == 1:
                UI.createTile(screen, 'normalTile', self.initX +
                              int(j)*self.unit, self.initY + int(i)*self.unit)
                UI.createBox(screen, self.block_1x, self.block_1y)
                UI.createBox(screen, self.block_2x, self.block_2y)
            # Other tile types...
    UI.createTile(screen, 'targetTile', self.targetX, self.targetY)


def edit_file(input_file, output_file):
    with open(input_file) as f:
        # Read the first three lines
        lines = f.readlines()
        n_rows, n_cols = map(int, lines[0].split())
        r, c = map(int, lines[1].split())
        new_r, new_c = map(int, lines[2].split())

        # Read the board
        board = [[int(x) for x in line.split()] for line in lines[3:]]

    # Increase the values in the first three lines
    n_rows += 4
    n_cols += 4
    r += 2
    c += 2
    new_r += 2
    new_c += 2

    # Add two extra columns of zeros to the left and right of the board
    board = [[0] * 2 + row + [0] * 2 for row in board]

    # Add two extra rows of zeros at the top and bottom of the board
    board = [[0] * n_cols] * 2 + board + [[0] * n_cols] * 2

    # Write the modified board to the output file
    with open(output_file, 'w') as f:
        f.write(f"{n_rows} {n_cols}\n")
        f.write(f"{r} {c}\n")
        f.write(f"{new_r} {new_c}\n")
        for row in board:
            f.write(' '.join(str(x) for x in row) + '\n')


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def run_bloxorz(args):
    cmd = ["python", "algorithm.py"] + args
    try:
        output = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Command {cmd} returned non-zero exit status {e.returncode}")
        print(e.output)
        return None
    else:
        # Parse the output to extract the list of solutions
        solutions = output.strip().split('\n')
        return solutions


def play(file_path):
    running = True
    move = 0
    map = Map(file_path)
    start = Position(map.boxPos[0], map.boxPos[1])
    goal = Position(map.targetPos[0], map.targetPos[1])
    mapAstar = MapAstar(map.size, start, goal, map.tile)
    start_time = time.time()
    edit_file(file_path, "Stage/Stage_1.txt")
    args = ["1", "BFS"]
    solutions = run_bloxorz(args)
    print(solutions)
    if 'SUCCESS!!!' in solutions:
        with open("Output/BFS_Stage_1.txt", 'r') as file:
            file_contents = file.read()
        print(file_contents)
    a_start_solver = AStarSolver(mapAstar)
    # tracemalloc.start()
    # start_time = time.time()
    print("Solution by A* algorithm:", a_start_solver.solve(),
          "\nin", time.time() - start_time, "seconds")
    # print(tracemalloc.get_traced_memory()[1])
    # tracemalloc.stop()
    while running:
        screen.blit(BG, (0, 0))
        stepText = my_font.render('Move {}'.format(move), False, (0, 0, 0))
        screen.blit(stepText, (415,50))
        render_map(screen, map)

        # stepText = my_font.render('{} {} {} {}'.format(block_1x, block_1y, block_2x, block_2y), False, (0, 0, 0))
        BACK_BUTTON = Button(image=pygame.image.load("assets/Back.png"), pos=(150, 750),
                             text_input="Back", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                running = False
            # Move block
            if event.type == pygame.KEYDOWN:
                keypress = event.key
                # Gameplay -> class Move
                if map.block_1x > map.block_2x:
                    (map.block_1x, map.block_2x) = (map.block_2x, map.block_1x)
                if map.block_1y > map.block_2y:
                    (map.block_1y, map.block_2y) = (map.block_2y, map.block_1y)
                if keypress == pygame.K_a or keypress == pygame.K_LEFT:
                    move += 1
                    if map.block_1x == map.block_2x:
                        if map.block_1y == map.block_2y:
                            map.block_2x -= map.unit
                            map.block_1x = map.block_2x - map.unit
                        else:
                            map.block_1x -= map.unit
                            map.block_2x -= map.unit
                    else:
                        map.block_1x -= unit
                        map.block_2x = map.block_1x
                    map.step += 1
                if keypress == pygame.K_d or keypress == pygame.K_RIGHT:
                    move += 1
                    if map.block_1x == map.block_2x:
                        if map.block_1y == map.block_2y:
                            map.block_1x += unit
                            map.block_2x = map.block_1x + unit
                        else:
                            map.block_1x += unit
                            map.block_2x += unit
                    else:
                        map.block_2x += unit
                        map.block_1x = map.block_2x
                    map.step += 1
                if keypress == pygame.K_w or keypress == pygame.K_UP:
                    move += 1
                    if map.block_1y == map.block_2y:
                        if map.block_1x == map.block_2x:
                            map.block_2y -= unit
                            map.block_1y = map.block_2y - unit
                        else:
                            map.block_1y -= unit
                            map.block_2y -= unit
                    else:
                        map.block_1y -= unit
                        map.block_2y = map.block_1y
                    map.step += 1
                if keypress == pygame.K_s or keypress == pygame.K_DOWN:
                    move += 1
                    if map.block_1y == map.block_2y:
                        if map.block_1x == map.block_2x:  # stand
                            map.block_1y += unit
                            map.block_2y = map.block_1y + unit
                        else:
                            map.block_1y += unit
                            map.block_2y += unit
                    else:
                        map.block_2y += unit
                        map.block_1y = map.block_2y
                    map.step += 1
                if keypress == pygame.K_r:  # reset round
                    blockX = map.initX + map.boxPos[0]*unit
                    blockY = map.initY + map.boxPos[1]*unit
                    map.step = 0
                # if event.key == pygame.K_q: # back step <- history
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    levelSelect()
        # check Win
        if map.block_1x == map.targetX and map.block_2x == map.targetX and map.block_1y == map.targetY and map.block_2y == map.targetY:
            stepText = my_font.render(('WIN !!!'), False, (0, 0, 0))
            screen.blit(stepText, (430,100))
        # Gameplay.checkWin(blockX, blockY, boxPos)

        for button in [BACK_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)
        pygame.display.update()


def levelSelect():
    while True:
        LEVELS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        LEVELS_TEXT = get_font(45).render("Level Selection", True, "Black")
        LEVELS_RECT = LEVELS_TEXT.get_rect(center=(500, 110))
        screen.blit(LEVELS_TEXT, LEVELS_RECT)

        ONE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(220, 260),
                            text_input="1", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_1.txt")
        TWO_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(360, 260),
                            text_input="2", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_2.txt")
        THREE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(500, 260),
                              text_input="3", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_3.txt")
        FOUR_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(640, 260),
                             text_input="4", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_4.txt")
        FIVE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(780, 260),
                             text_input="5", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_5.txt")
        SIX_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(220, 400),
                            text_input="6", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_6.txt")
        SEVEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(360, 400),
                              text_input="7", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_7.txt")
        EIGHT_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(500, 400),
                              text_input="8", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_8.txt")
        NINE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(640, 400),
                             text_input="9", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_9.txt")
        TEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(780, 400),
                            text_input="10", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_10.txt")
        # ELEV_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(220, 540),
        #                     text_input="11", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_1.txt")
        # TWELVE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(360, 540),
        #                     text_input="12", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_1.txt")
        # THIRDTEEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(500, 540),
        #                     text_input="13", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_1.txt")
        # FOURTEEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(640, 540),
        #                     text_input="14", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_1.txt")
        # FIFTEEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(780, 540),
        #                     text_input="15", font=get_font(40), base_color="#d7fcd4", hovering_color="White", level_file="testcase/test_1.txt")

        LEVELS_BACK = Button(image=None, pos=(500, 700),
                             text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Green")

        LEVELS_BACK.changeColor(LEVELS_MOUSE_POS)
        LEVELS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVELS_BACK.checkForInput(LEVELS_MOUSE_POS):
                    main_menu()
                if ONE_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(ONE_BUTTON.level_file)
                if TWO_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(TWO_BUTTON.level_file)
                if THREE_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(THREE_BUTTON.level_file)
                if FOUR_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(FOUR_BUTTON.level_file)
                if FIVE_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(FIVE_BUTTON.level_file)
                if SIX_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(SIX_BUTTON.level_file)
                if SEVEN_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(SEVEN_BUTTON.level_file)
                if EIGHT_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(EIGHT_BUTTON.level_file)
                if NINE_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(NINE_BUTTON.level_file)
                if TEN_BUTTON.checkForInput(LEVELS_MOUSE_POS):
                    play(TEN_BUTTON.level_file)
# , TWO_BUTTON, THREE_BUTTON, FOUR_BUTTON, FIVE_BUTTON,  SIX_BUTTON, SEVEN_BUTTON, EIGHT_BUTTON, NINE_BUTTON, TEN_BUTTON, ELEV_BUTTON, TWELVE_BUTTON, THIRDTEEN_BUTTON, FOURTEEN_BUTTON, FIFTEEN_BUTTON
        for button in [ONE_BUTTON, TWO_BUTTON, THREE_BUTTON, FOUR_BUTTON, FIVE_BUTTON, SIX_BUTTON, SEVEN_BUTTON, EIGHT_BUTTON, NINE_BUTTON, TEN_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)
        pygame.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("BLOXORZ", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 220))

        # PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 410),
        #                      text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        LEVELS_BUTTON = Button(image=pygame.image.load("assets/Level Rect.png"), pos=(500, 540),
                               text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 670),
                             text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [LEVELS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     play()
                if LEVELS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    levelSelect()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
