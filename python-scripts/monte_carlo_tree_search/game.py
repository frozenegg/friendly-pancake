import random
import math
import chess

class State:
	def __init__(self):
		self.board = chess.Board()

	def is_lose(self):
		return

	def is_draw(self):
		return self.board.is_stalemate() and self.board.is_insufficient_material()

	def is_done(self):
		return self.board.is_game_over()

	def next(self, action):
		move = chess.Move.from_uci(action)
		self.board.push(move)

	def legal_actions(self):
		legal_actions = []

		for i in board.legal_moves:
	  		legal_actions.append(str(i))

		return legal_actions

	def is_first_player(self):
		return board.turn == chess.WHITE

def random_action(state):
	legal_actions = []

	for i in state.board.legal_moves:
	  	legal_actions.append(str(i))

	return legal_actions[random.randint(0, len(legal_actions)-1)]


if __name__ == '__main__':
	state = State()

	while True:
		if state.is_done():
			break

		state.next(random_action(state))

		print(state.board)
		print()