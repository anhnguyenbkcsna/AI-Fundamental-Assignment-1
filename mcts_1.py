import numpy as np
from collections import defaultdict
from utils import load_data
from enum import Enum
from typing import List
from copy import deepcopy

size, boxPos, targetPos, tile = load_data("testcase/test_1.txt")

initial_state = [[boxPos[0], boxPos[1]], [boxPos[0], boxPos[1]]]
expected_state = [[targetPos[0], targetPos[1]], [targetPos[0], targetPos[1]]]


class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Move:
    @classmethod
    def moveUp(cls, state):
        new_state = deepcopy(state)
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
        new_state = deepcopy(state)
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
        new_state = deepcopy(state)
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
        new_state = deepcopy(state)
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


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.0
        self._results[result] += 1.0
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=np.sqrt(2)):
        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0.0)


class Bloxorz:
    def __init__(self, state):
        self.state = state

    def is_block_outbound(self, state):
        is_valid = (
            lambda num_block: 0 <= state[num_block][0] < size[0]
            and 0 <= state[num_block][1] < size[1]
        )
        if not is_valid(0) or not is_valid(1):
            return True
        is_block_1_outbound = tile[state[0][0]][state[0][1]] != 1
        is_block_2_outbound = tile[state[1][0]][state[1][1]] != 1
        return is_block_1_outbound or is_block_2_outbound

    def get_legal_actions(self):
        """
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        """
        legal_actions: List[Action] = []
        if not self.is_block_outbound(Move.moveUp(self.state)):
            legal_actions.append(Action.UP)
        if not self.is_block_outbound(Move.moveDown(self.state)):
            legal_actions.append(Action.DOWN)
        if not self.is_block_outbound(Move.moveLeft(self.state)):
            legal_actions.append(Action.LEFT)
        if not self.is_block_outbound(Move.moveRight(self.state)):
            legal_actions.append(Action.RIGHT)
        return legal_actions

    def is_game_over(self):
        """
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        """
        if len(self.get_legal_actions()) == 0 or self.state == expected_state:
            return True
        return False

    def game_result(self):
        """
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        """
        if self.state == expected_state:
            return 1
        elif self.is_block_outbound(self.state) or len(self.get_legal_actions()) == 0:
            return -1
        return 0

    def move(self, action):
        """
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        """
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
        return Bloxorz(state)


def main():
    root = MonteCarloTreeSearchNode(state=Bloxorz(initial_state))
    selected_node = root.best_action()
    return selected_node


print(main())
