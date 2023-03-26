from block import *


class Node:
    def __init__(self, block: Block, move: str = None, parent=None, f=0, g=0, h=0):
        self.block = block
        self.move = move
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h
