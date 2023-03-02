import pygame
class UI:
    def __init__(self):
        self.normalTile = (77,179,153)
        self.targetTile = (0,0,0)
        self.box = (157,104,60)
        
    def createTile(screen, color, posX, posY):
        if color == 'normalTile':
            pygame.draw.rect(screen, (64,99,46), pygame.Rect(posX+1, posY+1, 58, 58),  3)   # border
            pygame.draw.rect(screen, (77,179,153), pygame.Rect(posX+2, posY+2, 56, 56))     # inner
        if color == 'targetTile':
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(posX, posY, 60, 60))
        if color == 'orangeTile': # not assign num in map yet
            pygame.draw.rect(screen, (243,113,61), pygame.Rect(posX+2, posY+2, 56, 56))     # inner
    def createBox(screen, posX, posY):
        pygame.draw.rect(screen, (157,104,60), pygame.Rect(posX + 4, posY + 4, 52, 52)) 
    