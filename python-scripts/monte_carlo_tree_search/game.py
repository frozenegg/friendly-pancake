import random
import math
import chess
import numpy as np
import pickle

class State:
	def __init__(self):
		self.board = chess.Board()
		self.board_array = self.board_to_array()
		self.pieces = self.my_pieces()
		self.enemy_pieces = self.enemy_pieces()

	def board_to_array(self):
		flattened_board = ' '.join(str(self.board).split('\n'))
		flattened_board = np.array(flattened_board.split(' '))
		return flattened_board.reshape([8,-1])

	def my_pieces(self):
		board_array = self.board_array.flatten()
		white = ['P', 'R', 'N', 'B', 'Q', 'K']
		for i in range(len(board_array)):
			if board_array[i] in white:
				board_array[i] = white.index(board_array[i]) + 1
			else:
				board_array[i] = 0
		board_array = np.array([int(i) for i in board_array])
		return board_array.reshape([8,-1])

	def enemy_pieces(self):
		board_array = self.board_array.flatten()
		black = ['p', 'r', 'n', 'b', 'q', 'k']
		for i in range(len(board_array)):
			if board_array[i] in black:
				board_array[i] = black.index(board_array[i]) + 1
			else:
				board_array[i] = 0
		board_array = np.array([int(i) for i in board_array])
		return board_array.reshape([8,-1])

	def is_lose(self):
		board_array = self.board_array.flatten()
		return 'K' not in board_array

	def is_draw(self):
		return self.board.is_stalemate() and self.board.is_insufficient_material()

	def is_done(self):
		return self.board.is_game_over()

	def next(self, action_num):
		with open('action_list.txt', 'rb') as f:
			action_list = pickle.load(f)
		action = action_list[action_num]
		move = chess.Move.from_uci(action)
		self.board.push(move)
		self.convert_players()

	def convert_players(self):
		board_state = self.board_array[::-1]
		board_array = board_state.flatten()
		white = ['P', 'R', 'N', 'B', 'Q', 'K']
		black = ['p', 'r', 'n', 'b', 'q', 'k']
		for i in range(len(board_array)):
			if board_array[i] in white:
				board_array[i] = black[white.index(board_array[i])]
			elif board_array[i] in black:
				board_array[i] = white[black.index(board_array[i])]

		return board_array.reshape([8,-1])

	def legal_actions(self):
		legal_actions = []

		for i in self.board.legal_moves:
	  		legal_actions.append(str(i))

		try:
			with open('action_list.txt', 'rb') as f:
				action_list = pickle.load(f)
		except:
			action_list = []

		legal_action_num = []

		for action in legal_actions:
			if action in action_list:
				legal_action_num.append(action_list.index(action))
			else:
				legal_action_num.append(len(action_list))
				action_list.append(action)

		with open('action_list.txt', 'wb') as f:
			pickle.dump(action_list, f)

		return legal_action_num

	def is_first_player(self):
		return self.board.turn == chess.WHITE

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