from random import choice
from mcts_2 import MCTS, Node
from utils import load_data
from enum import Enum
import copy

size, boxPos, targetPos, terrain = load_data("testcase/test_1.txt")

initial_state = [[boxPos[0], boxPos[1]], [boxPos[0], boxPos[1]]]
expected_state = [[targetPos[0], targetPos[1]], [targetPos[0], targetPos[1]]]


def is_state_valid(state):
    is_valid = (
        lambda num_block: 0 <= state[num_block][0] < size[0]
        and 0 <= state[num_block][1] < size[1]
    )
    if not is_valid(0) or not is_valid(1):
        return False
    is_block_1_outbound = terrain[state[0][0]][state[0][1]] != 1
    is_block_2_outbound = terrain[state[1][0]][state[1][1]] != 1
    return not (is_block_1_outbound or is_block_2_outbound)


class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Move:
    @classmethod
    def moveUp(cls, state):
        new_state = copy.deepcopy(state)
        if new_state[0][0] == new_state[1][0]:
            if new_state[0][1] == new_state[1][1]:
                new_state[0][0] -= 2
                new_state[1][0] -= 1
            else:
                new_state[0][0] += 1
                new_state[1][0] += 2
        else:
            new_state[0][0] -= 1
            new_state[1][0] -= 1
        return new_state

    @classmethod
    def moveDown(cls, state):
        new_state = copy.deepcopy(state)
        if new_state[0][0] == new_state[1][0]:
            if new_state[0][1] == new_state[1][1]:
                new_state[0][0] += 1
                new_state[1][0] += 2
            else:
                new_state[0][0] += 1
                new_state[1][0] += 2
        else:
            new_state[0][0] += 1
            new_state[1][0] += 1
        return new_state

    @classmethod
    def moveLeft(cls, state):
        new_state = copy.deepcopy(state)
        if new_state[0][0] == new_state[1][0]:
            if new_state[0][1] == new_state[1][1]:
                new_state[0][1] -= 2
                new_state[1][1] -= 1
            else:
                new_state[0][1] -= 1
                new_state[1][1] -= 2
        else:
            new_state[0][1] -= 1
            new_state[1][1] -= 1
        return new_state

    @classmethod
    def moveRight(cls, state):
        new_state = copy.deepcopy(state)
        if new_state[0][0] == new_state[1][0]:
            if new_state[0][1] == new_state[1][1]:
                new_state[0][1] += 1
                new_state[1][1] += 2
            else:
                new_state[0][1] += 2
                new_state[1][1] += 1
        else:
            new_state[0][1] += 1
            new_state[1][1] += 1
        return new_state


class Bloxorz(Node):
    def __init__(self, state, terminal=False):
        self.state = state
        self.terminal = terminal

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state))

    def __eq__(self, other):
        return self.state == other.state

    def find_children(self):
        "All possible successors of this board state"
        if self.terminal:
            return set()
        return {
            self.make_move(action) for action in list(Action) if self.make_move(action)
        }

    def make_move(self, action: Action):
        state = None
        if action == Action.UP:
            state = Move.moveUp(self.state)
        elif action == Action.DOWN:
            state = Move.moveDown(self.state)
        elif action == Action.LEFT:
            state = Move.moveLeft(self.state)
        elif action == Action.RIGHT:
            state = Move.moveRight(self.state)
        else:
            raise ValueError("Invalid action")
        if is_state_valid(state):
            if state == expected_state:
                return Bloxorz(state, terminal=True)
            return Bloxorz(state)
        else:
            return None

    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        if self.terminal:
            return None
        arr = self.find_children()
        return choice(list(arr))

    def is_terminal(self):
        "Returns True if the node has no children"
        return self.terminal

    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        if not self.terminal:
            raise RuntimeError(f"Reward called on nonterminal board {self.state}")
        if not is_state_valid(self.state):
            raise RuntimeError(f"Reward called on invalid board {self.state}")
        if self.state == expected_state:
            return 1
        return 0


def main():
    tree = MCTS()
    board = Bloxorz(initial_state)
    while True:
        if board.terminal:
            break
        tree.do_rollout(board)
        board = tree.choose(board)
        print(board.state)
        if board.terminal:
            break


main()
