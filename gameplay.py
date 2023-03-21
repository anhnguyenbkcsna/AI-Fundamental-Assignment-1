import pygame

unit = 60 # change px to square
class Gameplay:
	def __init__(self):
		print('Init gameplay')
  
	def checkWin(blockX, blockY, target): # if win -> pass False to 'running' in main.py
		if blockX == target[0] and blockY == target[1]:
			return False
		else:
			return True
	
	def checkBoundary(blockX, blockY, map): # if true, continue to play the game
		return True

# can not import to use in main.py
class Move:
	def __init__(self):
		keypress = self.keypress
	def moveUp(block_1y,block_2y):
		if block_1y == block_2y: #stand
			block_1y -= unit
			block_2y = block_1y - unit
		else:
			block_2y -= unit
			block_1y = block_2y
	def moveDown(block_1y,block_2y):
		if block_1y == block_2y: #stand
			block_1y += unit
			block_2y = block_1y + unit
		else:
			block_2y += unit
			block_1y = block_2y
	def moveLeft(block_1x, block_2x):
		if block_1x == block_1x: #stand
			block_1x -= unit
			block_2y = block_1x - unit
		else:
			block_2y -= unit
			block_1x = block_2y
	def moveRight(block_1x, block_2x):
		if block_1x == block_1x: #stand
			block_1x += unit
			block_2y = block_1x + unit
		else:
			block_2y += unit
			block_1x = block_2y