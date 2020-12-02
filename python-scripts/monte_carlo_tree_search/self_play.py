from game import State
from pv_mcts import pv_mcts_scores
# from dual_network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle
import os

SP_GAME_COUNT = 500
SP_TEMPERATURE = 1.0

def first_player_value(ended_state):
	if ended_state.is_lose():
		return -1 if ended_state.is_first_player() else 1
	return 0

def write_data(history):
	now = datetime.now()
	os.makedirs('./data/', exist_ok=True)
	path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
	with open(path, mode='wb') as f:
		pickle.dump(history, f)

def play(model):
	history = []
	state = State()

	while True:
		if state.is_done():
			break

		scores = pv_mcts_scores(model, state, SP_TEMPERATURE)

		with open('action_list.txt', 'rb') as f:
			action_list = pickle.load(f)

		# print('action_list:', len(action_list))

		policies = np.zeros(len(action_list))
		# for action_num, policy in zip(state.legal_actions(), scores):
		# 	policies[action_num] = policy

		# print('size check', len(policies), len(scores))

		legal_actions = state.legal_actions()

		for i in range(len(legal_actions)):
			policies[legal_actions[i]] = scores[i]
			# print(policies)
		# print('policies:', policies)
		history.append([[state.pieces, state.enemy_pieces], policies, None])

		# action_list_num = np.arange(len(action_list))
		# action_num = np.random.choice(action_list_num, p=scores)
		action_num = np.random.choice(legal_actions, p=scores)
		# print(action_num)
		state.next(action_num)

	value = first_player_value(state)
	for i in range(len(history)):
		history[i][2] = value
		value = -value
	return history

def self_play():
	history = []
	model = load_model('./model/best.h5')

	for i in range(SP_GAME_COUNT):
		h = play(model)
		history.extend(h)
		# print(history)

		print('\rSelfPlay {}/{}'.format(i+1, SP_GAME_COUNT), end='')
	print('')

	write_data(history)

	K.clear_session()
	del model

if __name__ == '__main__':
	self_play()
