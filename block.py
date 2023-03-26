class Block:
    def __init__(self, pos1: tuple, pos2: tuple):
        if pos1[0] > pos2[0]:
            pos1[0], pos2[0] = pos2[0], pos1[0]
        if pos1[1] > pos2[1]:
            pos1[1], pos2[1] = pos2[1], pos1[1]
        self.pos1 = pos1
        self.pos2 = pos2

    def left(self):
        if self.pos1[0] == self.pos2[0]:
            if self.pos1[1] == self.pos2[1]:
                self.pos2 = (self.pos2[0] - 1, self.pos2[1])
                self.pos1 = (self.pos2[0] - 1, self.pos1[1])
            else:
                self.pos1 = (self.pos1[0] - 1, self.pos1[1])
                self.pos2 = (self.pos2[0] - 1, self.pos2[1])
        else:
            self.pos1 = (self.pos1[0] - 1, self.pos1[1])
            self.pos2 = (self.pos1[0], self.pos2[1])
        return Block(self.pos1, self.pos2)

    def right(self):
        if self.pos1[0] == self.pos2[0]:
            if self.pos1[1] == self.pos2[1]:
                self.pos1 = (self.pos1[0] + 1, self.pos1[1])
                self.pos2 = (self.pos1[0] + 1, self.pos2[1])
            else:
                self.pos1 = (self.pos1[0] + 1, self.pos1[1])
                self.pos2 = (self.pos2[0] + 1, self.pos2[1])
        else:
            self.pos2 = (self.pos2[0] + 1, self.pos2[1])
            self.pos1 = (self.pos2[0], self.pos1[1])
        return Block(self.pos1, self.pos2)

    def up(self):
        if self.pos1[1] == self.pos2[1]:
            if self.pos1[0] == self.pos2[0]:
                self.pos2 = (self.pos2[0], self.pos2[1] - 1)
                self.pos1 = (self.pos1[0], self.pos2[1] - 1)
            else:
                self.pos1 = (self.pos1[0], self.pos1[1] - 1)
                self.pos2 = (self.pos2[0], self.pos2[1] - 1)
        else:
            self.pos1 = (self.pos1[0], self.pos1[1] - 1)
            self.pos2 = (self.pos2[0], self.pos1[1])
        return Block(self.pos1, self.pos2)

    def down(self):
        if self.pos1[1] == self.pos2[1]:
            if self.pos1[0] == self.pos2[0]:
                self.pos1 = (self.pos1[0], self.pos1[1] + 1)
                self.pos2 = (self.pos2[0], self.pos1[1] + 1)
            else:
                self.pos1 = (self.pos1[0], self.pos1[1] + 1)
                self.pos2 = (self.pos2[0], self.pos2[1] + 1)
        else:
            self.pos2 = (self.pos2[0], self.pos2[1] + 1)
            self.pos1 = (self.pos1[0], self.pos2[1])
        return Block(self.pos1, self.pos2)
