import random
import math
import chess
import numpy as np
import pickle

board = chess.Board()

# print(board.legal_moves)

for i in range(3):
	legal_action = []

	for j in board.legal_moves:
	  legal_action.append(str(j))

	print(legal_action)

	action = chess.Move.from_uci(legal_action[0])
	board.push(action)

# 	print(board)

# 	print(board.turn == chess.WHITE)

flattened_board = ' '.join(str(board).split('\n'))
flattened_board = np.array(flattened_board.split(' '))
board_array = flattened_board.reshape([8,-1])
print(board_array)
print()

def convert_players(board_state):
	board_state = board_state[::-1]
	board_array = board_state.flatten()
	white = ['P', 'R', 'N', 'B', 'Q', 'K']
	black = ['p', 'r', 'n', 'b', 'q', 'k']
	for i in range(len(board_array)):
		if board_array[i] in white:
			board_array[i] = black[white.index(board_array[i])]
		elif board_array[i] in black:
			board_array[i] = white[black.index(board_array[i])]

	return board_array.reshape([8,-1])

print(convert_players(board_array))

def my_pieces(board_array):
	board_array = board_array.flatten()
	white = ['P', 'R', 'N', 'B', 'Q', 'K']
	for i in range(len(board_array)):
		if board_array[i] in white:
			board_array[i] = white.index(board_array[i]) + 1
		else:
			board_array[i] = 0
	board_array = np.array([int(i) for i in board_array])
	return board_array.reshape([8,-1])

def enemy_pieces(board_array):
	board_array = board_array.flatten()
	black = ['p', 'r', 'n', 'b', 'q', 'k']
	for i in range(len(board_array)):
		if board_array[i] in black:
			board_array[i] = black.index(board_array[i]) + 1
		else:
			board_array[i] = 0
	board_array = np.array([int(i) for i in board_array])
	return board_array.reshape([8,-1])

print(my_pieces(board_array))
print(enemy_pieces(board_array))

try:
	with open('action_list.txt', 'rb') as f:
		action_list = pickle.load(f)
except:
	action_list = []

legal_action_num = []

for action in legal_action:
	if action in action_list:
		legal_action_num.append(action_list.index(action))
	else:
		legal_action_num.append(len(action_list))
		action_list.append(action)

with open('action_list.txt', 'wb') as f:
	pickle.dump(action_list, f)

array = ['a', 'b']
print('a' not in array)