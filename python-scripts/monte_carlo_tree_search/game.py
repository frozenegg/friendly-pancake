import random
import math

class State:
    def __init__(self, pieces=None, enemy_pieces=None):
        self.pieces = pieces if pieces != None else [0] * 9
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * 9

    def piece_count(self.pieces)

def random_action(state):

def alpha_beta(state, alpha, beta):

def alpha_beta_action(state):

def playout(state):

def argmax(collection):

def mcts_action(state):

if __name__ == '__main__':
    state = State()

    while True:
        if state.is_done():
            break

        state = state.next(random_action(state))

        print(state)
        print()
