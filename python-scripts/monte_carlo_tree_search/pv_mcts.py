from game import State
from dual_network import DN_INPUT_SHAPE
from math import sqrt
from tensorflow.keras.models import load_model
from pathlib import Path
import numpy as np
import pickle
import chess

PV_EVALUATE_COUNT = 50

def predict(model, state):
	a, b, c = DN_INPUT_SHAPE
	x = np.array([state.pieces, state.enemy_pieces])
	x = x.reshape(c, a, b).transpose(1,2,0).reshape(1, a, b, c)

	y = model.predict(x, batch_size=1)
	# print(y[0][0], len(y[0][0]))
	# print(list(state.legal_actions()))
	# policies = y[0][0][list(state.legal_actions())]


	# print(list(state.legal_actions()))
	# print(legal_actions_binary)
	legal_actions = list(state.legal_actions())

	with open('action_list.txt', 'rb') as f:
		action_list = pickle.load(f)

	legal_actions_binary = np.zeros(len(action_list))

	for i in legal_actions:
		legal_actions_binary[i] = 1
	legal_actions_binary = np.array(legal_actions_binary, dtype='int32')
	# print(legal_actions_binary, legal_actions_binary.dtype)

	# print('y:', y[0][0], len(y[0][0]))

	# policies = y[0][0][legal_actions_binary]
	policies = [y[0][0][i] if legal_actions_binary[i] == 1 else 0 for i in range(len(legal_actions_binary))]
	print('policies:', policies)
	try:
		policies /= sum(policies)
	except:
		policies = np.ones(len(policies))

	value = y[1][0][0]
	# print('polices:', policies)
	# print('value:', value)
	return policies, value

def nodes_to_scores(nodes):
	scores = []
	for c in nodes:
		scores.append(c.n)
	# print('nodes to scores:', scores)
	return scores

def pv_mcts_scores(model, state, temperature):
	class node:
		def __init__(self, state, p):
			self.state = state
			self.p = 0
			self.w = 0
			self.n = 0
			self.child_nodes = None

		def evaluate(self):
			if self.state.is_done():
				# print(self.state.board)
				# print('done', self.state.is_lose())
				value = -1 if self.state.is_lose() else 0

				self.w += value
				self.n += 1
				return value

			if not self.child_nodes:
				# print('not child nodes')
				policies, value = predict(model, self.state)
				self.w += value
				self.n += 1

				# print('policies:', policies)

				with open('action_list.txt', 'rb') as f:
					action_list = pickle.load(f)

				self.child_nodes = []
				legal_actions = self.state.legal_actions()
				# for action_num, policy in zip(self.state.legal_actions(), policies):
				# 	self.state.next(action_num)
				# 	self.child_nodes.append(node(self.state.board_array, policy))
				# print('legal_actions length before loop:', len(legal_actions))
				for action_num in legal_actions:
					original_state = self.state.board.fen()
					# print('original:' + str(action_num) + '\n', chess.Board(original_state))
					self.state.next(action_num)
					policy = policies[action_num]
					self.child_nodes.append(node(self.state, policy))
					self.state.board = chess.Board(original_state)
					# print('check board:' + str(action_num) + '\n', self.state.board)
					# print('added: ' + str(action_num) + ' to child nodes')
					print(self.state.board)
				# print('child node length:', len(self.child_nodes))
				# print('legal_actions length:', len(legal_actions))
				return value
			else:
				# print('else')
				value = -self.next_child_node().evaluate()

				self.w += value
				self.n += 1
				# print('n + 1 to be ', self.n)
				# print('value:', value)
				return value

		def next_child_node(self):
			C_PUCT = 1.0
			t = sum(nodes_to_scores(self.child_nodes))
			pucb_values = []
			for child_node in self.child_nodes:
				pucb_values.append((-child_node.w / child_node.n if child_node.n else 0.0) + C_PUCT * child_node.p * sqrt(t) / (1 + child_node.n))
			# print('pucb values:', pucb_values)
			return self.child_nodes[np.argmax(pucb_values)]

	root_node = node(state, 0)

	for _ in range(PV_EVALUATE_COUNT):
		root_node.evaluate()

	scores = nodes_to_scores(root_node.child_nodes)
	# print('scores:', scores)
	# print(temperature)
	if temperature == 0:
		action_num = np.argmax(scores)
		scores = np.zeros(len(scores))
		scores[action_num] = 1
	else:
		scores = boltzman(scores, temperature)

	return scores

def pv_mcts_action_num(model, temperature=0):
	def pv_mcts_action_num(state):
		scores = pv_mcts_scores(model, state, temperature)
		return np.random.choice(state.legal_actions(), p=scores)
	return pv_mcts_action_num

def boltzman(xs, temperature):
	xs = [x ** (1 / temperature) for x in xs]
	return [x / sum(xs) for x in xs]

if __name__ == '__main__':
	path = sorted(Path('./model').glob('*.h5'))[-1]
	model = load_model(str(path))

	state = State()

	next_action = pv_mcts_action_num(model, 1.0)

	while True:
		if state.is_done():
			break

		action = next_action(state)
		state.next(action_num)

		print(state.board)
