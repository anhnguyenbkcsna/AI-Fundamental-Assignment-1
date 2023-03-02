import pygame

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

	