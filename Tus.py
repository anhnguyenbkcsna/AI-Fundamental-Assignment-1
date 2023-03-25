import pygame
import sys
from ui import *
from gameplay import *
from utils import load_data
from button import *

#intia pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 48)

#create screeb
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Bloxor")
pygame.display.set_icon(pygame.image.load('./assets/cube64.png'))

# import assets
blockImage = pygame.image.load('./assets/square.png')
BG = pygame.image.load("img/bg.jpg")

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

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    global step, isStand, isWin, keypress, block_1x, block_2x, block_1y, block_2y, targetX, targetY, lieX, lieY, standX, standY, blockX, blockY, initX, initY, size, boxPos, targetPos, tile
    running = True
    while running:
        screen.blit(BG, (0, 0))
        # stepText = my_font.render('Move {}'.format(step), False, (0, 0, 0))
        stepText = my_font.render('{} {} {} {}'.format(block_1x, block_2x, block_1y, block_2y), False, (0, 0, 0))
        screen.blit(stepText, (430,100))
        # stepText = my_font.render('{} {} {} {}'.format(block_1x, block_1y, block_2x, block_2y), False, (0, 0, 0))
        # screen.blit(stepText, (430,100))
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
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_menu()

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
                            text_input="1", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        TWO_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(360, 260), 
                            text_input="2", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        THREE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(500, 260), 
                            text_input="3", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        FOUR_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(640, 260), 
                            text_input="4", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        FIVE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(780, 260), 
                            text_input="5", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SIX_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(220, 400), 
                            text_input="6", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SEVEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(360, 400), 
                            text_input="7", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        EIGHT_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(500, 400), 
                            text_input="8", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        NINE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(640, 400), 
                            text_input="9", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        TEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(780, 400), 
                            text_input="10", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        ELEV_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(220, 540), 
                            text_input="11", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        TWELVE_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(360, 540), 
                            text_input="12", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        THIRDTEEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(500, 540), 
                            text_input="13", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        FOURTEEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(640, 540), 
                            text_input="14", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        FIFTEEN_BUTTON = Button(image=pygame.image.load("assets/level/1.png"), pos=(780, 540), 
                            text_input="15", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
       


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

        for button in [ONE_BUTTON, TWO_BUTTON, THREE_BUTTON, FOUR_BUTTON, FIVE_BUTTON,  SIX_BUTTON, SEVEN_BUTTON, EIGHT_BUTTON, NINE_BUTTON, TEN_BUTTON, ELEV_BUTTON, TWELVE_BUTTON, THIRDTEEN_BUTTON, FOURTEEN_BUTTON, FIFTEEN_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)
        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("BLOXORZ", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 220))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 410), 
                            text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        LEVELS_BUTTON = Button(image=pygame.image.load("assets/Level Rect.png"), pos=(500, 540), 
                            text_input="LEVELS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 670), 
                            text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, LEVELS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if LEVELS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    levelSelect()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()