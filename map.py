import json


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dx(self, d):
        return Position(self.x + d, self.y)

    def dy(self, d):
        return Position(self.x, self.y + d)

    def isEqual(self, p):
        return self.x == p.x and self.y == p.y

    def __str__(self):
        return json.dumps([self.x, self.y])


class Block:
    def __init__(self, pos1: Position, pos2: Position):
        self.pos1 = pos1
        self.pos2 = pos2

    def left(self):
        if self.pos1.x == self.pos2.x:
            if self.pos1.y == self.pos2.y:
                return Block(self.pos1.dx(-2), self.pos2.dx(-1))
            else:
                return Block(self.pos1.dx(-1), self.pos2.dx(-1))
        else:
            return Block(self.pos1.dx(-1), self.pos2.dx(-2))

    def right(self):
        if self.pos1.x == self.pos2.x:
            if self.pos1.y == self.pos2.y:
                return Block(self.pos1.dx(1), self.pos2.dx(2))
            else:
                return Block(self.pos1.dx(1), self.pos2.dx(1))
        else:
            return Block(self.pos1.dx(2), self.pos2.dx(1))

    def up(self):
        if self.pos1.y == self.pos2.y:
            if self.pos1.x == self.pos2.x:
                return Block(self.pos1.dy(-2), self.pos2.dy(-1))
            else:
                return Block(self.pos1.dy(-1), self.pos2.dy(-1))
        else:
            return Block(self.pos1.dy(-1), self.pos2.dy(-2))

    def down(self):
        if self.pos1.y == self.pos2.y:
            if self.pos1.x == self.pos2.x:
                return Block(self.pos1.dy(1), self.pos2.dy(2))
            else:
                return Block(self.pos1.dy(1), self.pos2.dy(1))
        else:
            return Block(self.pos1.dy(2), self.pos2.dy(1))

    def isEqual(self, b):
        return self.pos1.isEqual(b.pos1) and self.pos2.isEqual(b.pos2)

    def __str__(self):
        return json.dumps([str(self.pos1), str(self.pos2)])


class Map:
    def __init__(self, size, start: Position, goal: Position, tile):
        self.size = size
        self.start = start
        self.goal = goal
        self.tile = tile

    def validMove(self, x: Block):
        up = x.up()
        down = x.down()
        right = x.right()
        left = x.left()
        list = []
        if self.isInMap(up):
            list.append((up, "U"))
        if self.isInMap(down):
            list.append((down, "D"))
        if self.isInMap(right):
            list.append((right, "R"))
        if self.isInMap(left):
            list.append((left, "L"))
        return list

    def isInMap(self, b: Block):
        if b.pos1.x < 0 or b.pos2.x < 0 or b.pos1.y < 0 or b.pos2.y < 0:
            return False
        if b.pos1.y >= self.size[0] or b.pos2.y >= self.size[0]:
            return False
        if b.pos1.x >= self.size[1] or b.pos2.x >= self.size[1]:
            return False
        if self.tile[b.pos1.y][b.pos1.x] == 1 and self.tile[b.pos2.y][b.pos2.x] == 1:
            return True
        return False
