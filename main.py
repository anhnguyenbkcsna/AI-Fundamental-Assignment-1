import pygame

# intialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Bloxor")
# pygame.display.set_icon(pygame.image.load('filename'))

# import assets
blockImage = pygame.image.load('./assets/square.png')

# Global variable
initX = 480
lieX = 24
blockX = initX

initY = 380
lieY = 14
standY = -32
blockY = initY

pos = 64
step = 0
isStand = True # check if block Stand
keypress = ''


def block(x, y, isStand, keypress):
    # wrong way to lie
    screen.blit(blockImage, (x, y)) # cube1
    if isStand == True:
        screen.blit(blockImage, (x, y + standY)) # cube2
    else:
        screen.blit(blockImage, (x+ lieX, y + lieY))
# Game loop
running = True
while running: 
    screen.fill((255,255,255)) # background
    
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False
        # Move block
        if event.type == pygame.KEYDOWN:
            keypress = event.key
            isStand = not isStand
            step += 1
            if keypress == pygame.K_a or keypress == pygame.K_LEFT:
                blockX -= pos
            if keypress == pygame.K_d or keypress == pygame.K_RIGHT:
                blockX += pos
            if keypress == pygame.K_w or keypress == pygame.K_UP:
                blockY -= pos
            if keypress == pygame.K_s or keypress == pygame.K_DOWN:
                blockY += pos
            if keypress == pygame.K_r: # reset round
                blockX = initX
                blockY = initY
            # if event.key == pygame.K_q: # back step <- history
        
        # boundary? 

    
    block(blockX, blockY, isStand, keypress) #draw block
    pygame.display.update()