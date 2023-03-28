from map import *


class Node:
    def __init__(self, block: Block, move: str, parent, f=0, g=0, h=0):
        self.f = f
        self.g = g
        self.h = h
        self.block = block
        self.move = move
        self.parent = parent

    def isEqual(self, n):
        return self.block.isEqual(n.block)

    def __str__(self):
        json.dumps([str(self.block), str(self.move), str(
            self.parent), str(self.f), str(self.g), str(self.h)])

# Sử dụng Chebyshev distance


class AStarSolver:
    def __init__(self, map: MapAstar):
        self.map = map

    def solve(self):
        open_list = []
        close_list = []

        start = self.map.start
        start_block = Block(start, start)
        start_node = Node(start_block, None, None, 0, 0, 0)
        goal = self.map.goal
        goal_block = Block(goal, goal)

        open_list.append(start_node)
        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0

            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            close_list.append(current_node)

            if current_node.block.isEqual(goal_block):
                paths = []
                current = current_node

                while current is not None:
                    paths.append(current.move)
                    current = current.parent
                # return True
                paths.reverse()
                paths.pop(0)
                return paths
            children = self.get_children(current_node)

            for child in children:
                if child in close_list:
                    continue

                child.g = current_node.g + 1
                h1 = max(abs(child.block.pos1.x - goal_block.pos1.x),
                         abs(child.block.pos1.y - goal_block.pos1.y))
                h2 = max(abs(child.block.pos2.x - goal_block.pos2.x),
                         abs(child.block.pos2.y - goal_block.pos2.y))
                child.h = max(h1, h2)

                child.f = child.g + child.h

                for node in open_list:
                    if child.isEqual(node) and child.g > node.g:
                        continue

                open_list.append(child)

    def get_children(self, node: Node):
        children = []
        for (b, move) in self.map.validMove(node.block):
            child = Node(b, move, node)
            children.append(child)
        return children
