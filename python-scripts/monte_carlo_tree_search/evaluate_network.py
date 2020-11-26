from game import State
from pv_mcts import pv_mcts_action_num
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
from shutil import copy
import numpy as np

EN_GAME_COUNT = 10
EN_TEMPERATURE = 1.0

def first_player_point(ended_state):
	if ended_state.is_lose():
		return 0 if ended_state.is_first_player() else 1
	return 0.5

def play(next_actions_num):
	state = State()

	while True:
		if state.is_done():
			break

		next_action_num = next_actions_num[0] if state.is_first_player() else next_actions_num[1]
		action_num = next_action_num(state)

		state.next(action_num)

	return first_player_point(state)

def update_best_player():
	copy('./model/latest.h5', './model/best.h5')
	print('Change BestPlayer')

def evaluate_network():
	model0 = load_model('./model/latest.h5')
	model1 = load_model('./model/best.h5')

	next_action_num0 = pv_mcts_action_num(model0, EN_TEMPERATURE)
	next_action_num1 = pv_mcts_action_num(model1, EN_TEMPERATURE)
	next_actions_num = (next_action_num0, next_action_num1)

	total_point = 0
	for i in range(EN_GAME_COUNT):
		if i % 2 == 0:
			total_point += play(next_actions_num)
		else:
			total_point += 1 - play(list(reversed(next_actions_num)))

		print('\rEvaluate {}/{}'.format(i + 1, EN_GAME_COUNT), end='')
	print('')

	average_point = total_point / EN_GAME_COUNT
	print('AveragePoint', average_point)

	K.clear_session()
	del model0
	del model1

	if average_point > 0.5:
		update_best_player()
	# 	return True
	# else:
	# 	return False

if __name__ == '__main__':
	evaluate_network()