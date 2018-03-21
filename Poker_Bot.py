### MODULE NAME: 	Poker_Bot
### 
### DESCRIPTION: 	This module contains functions and classes for the poker bot.
###
### REFERENCES: 	
### 	[S&B 2018]	 	- "Reinforcement Learning: An Introduction" by Sutton & Barto (2018)

from deuces import Card
from deuces import Deck
from deuces import Evaluator
import pickle
import random

STATES = [(), ('Ch','B'), ('B','B'), ('Ch','B','B','B'), ('B','B','B','B'), ('Ch',), ('B',), ('Ch','B','B'), ('B','B','B'), ('Ch','B','B','B','B')]
ACTIONS = [('Ch','B'), ('F','C','B'), ('F','C','B'), ('F','C','B'), ('F','C'), ('Ch','B'), ('F','C','B'), ('F','C','B'), ('F','C','B'), ('F','C')]
STATE_TYPE_1 = [(), ('Ch',)]
STATE_TYPE_2 = [('Ch','B'), ('Ch','B','B','B'), ('B','B'), ('Ch','B','B'), ('B',), ('B','B','B')]
STATE_TYPE_3 = [('B','B','B','B'), ('Ch','B','B','B','B')]

# CLASS NAME:	Game_State
#
# DESCRIPTION: 	This class keeps track of the current state of the game
#
# ref1

class Game_State:
	### CONSTRUCTORS

	def __init__(self):
		self.player_cards = None
		self.opponent_cards = None
		self.flop_cards = None
		self.action_round = []
		self.valid_actions = ['Ch','B','F','C'] # Set of valid actions

	### FUNCTIONS FOR CHANGING GAME_STATE

	def clear_state(self):
		self.player_cards = None
		self.opponent_cards = None
		self.flop_cards = None
		self.action_round = []

	def set_player_cards(self, player_cards):
		self.player_cards = player_cards

	def set_opponent_cards(self, opponent_cards):
		self.opponent_cards = opponent_cards

	def set_flop(self, flop_cards):
		self.flop_cards = flop_cards

	def append_action(self, action):
		if action not in self.valid_actions:
			print('ERROR: Not valid action.')
		elif self.action_round.count('B') == 4 and action == 'B':
			print('ERROR: At most four bets/raises.')
		else:
			self.action_round.append(action)

	### FUNCTIONS FOR PRINTING GAME_STATE

	def print_player_cards(self):
		try:
			Card.print_pretty_cards(self.player_cards)
		except TypeError, e:
			print('ERROR: Something went wrong. Make sure that all required cards are defined.')

	def print_opponent_cards(self):
		try:
			Card.print_pretty_cards(self.opponent_cards)
		except TypeError, e:
			print('ERROR: Something went wrong. Make sure that all required cards are defined.')

	def print_flop(self):
		try:
			Card.print_pretty_cards(self.flop_cards)
		except TypeError, e:
			print('ERROR: Something went wrong. Make sure that all required cards are defined.')

	def print_player_hand(self):
		try:
			Card.print_pretty_cards(self.player_cards + self.flop_cards)
		except TypeError, e:
			print('ERROR: Something went wrong. Make sure that all required cards are defined.')

	def print_opponent_hand(self):
		try:
			Card.print_pretty_cards(self.opponent_cards + self.flop_cards)
		except TypeError, e:
			print('ERROR: Something went wrong. Make sure that all required cards are defined.')

	def get_possible_actions(self):
		if tuple(self.action_round) in STATE_TYPE_1:
			return ['Ch','B']
		elif tuple(self.action_round) in STATE_TYPE_2:
			return ['F','C','B']
		elif tuple(self.action_round) in STATE_TYPE_3:
			return ['F','C']
		else:
			return []

	def get_current_state_id(self):
		# current_state_id encodes the current state as follows:
		# current_state_id[0]: Indicates whether or not the player's two cards are the same suit
		# current_state_id[1]: Value of the player's high card
		# current_state_id[2]: Value of the player's low card
		# current_state_id[3]: The actions taken, as stored in self.action_round
		if Card.get_rank_int(self.player_cards[0]) >= Card.get_rank_int(self.player_cards[1]):
			high_card = Card.get_rank_int(self.player_cards[0])
			low_card = Card.get_rank_int(self.player_cards[1])
		else:
			high_card = Card.get_rank_int(self.player_cards[1])
			low_card = Card.get_rank_int(self.player_cards[0])
		is_same_suit = Card.get_suit_int(self.player_cards[0]) == Card.get_suit_int(self.player_cards[1])
		current_state_id = (int(is_same_suit),high_card,low_card,tuple(self.action_round))
		return current_state_id

	### FUNCTIONS FOR EVALUATION

	def is_winner(self):
		# This function return 1 if the player wins, 0 if it is a draw, and -1 if the opponent wins.
		try:
			player_hand_str = Evaluator().evaluate(self.flop_cards, self.player_cards)
			opponent_hand_str = Evaluator().evaluate(self.flop_cards, self.opponent_cards)
		except TypeError, e:
			print('ERROR: Something went wrong. Make sure that all required cards are defined.')
		if player_hand_str < opponent_hand_str: # Remember that lower is better!
			return 1
		elif player_hand_str == opponent_hand_str:
			return 0
		else:
			return -1

	# Returns payoff for player. Assums bet size are all $1.
	def payoff(self):
		pot_size = self.action_round.count('B')
		if self.is_winner():
			return pot_size
		else:
			return 0.0

	# Returns payoff for opponent. Assums bet size are all $1.
	def opponent_payoff(self):
		pot_size = self.action_round.count('B')
		if not self.is_winner():
			return pot_size
		else:
			return 0.0
# End of Game_State class


# CLASS NAME:	Policy
# 
# DESCRIPTION: 	This class defines a policy on the Game_State states
# 
# NOTES:
# 	Note 1 		- The variable "states" keeps track of all possible states of the action_round 
# 				  variable for which we might need to take an action. The "actions" variable keeps
#				  track of all possible actions for each state in the "states" variable. Together,
#				  these two lists are used to build a dictionary which holds the policy_function.
#
# ref2

class Policy:
	### CONSTRUCTORS

	# Construct policy from policy dictionary
	def __init__(self, policy_dict):
		self.policy_function = policy_dict

	# Construct uniform policy
	@classmethod
	def create_uniform(cls):
		policy_dict = {}
		for is_same_suit in range(2):
			for high_card in range(13):
				for low_card in range(13):
					for state_idx in range(len(STATES)):
						for action in ACTIONS[state_idx]:
							full_state = (is_same_suit, high_card, low_card, STATES[state_idx], action)
							policy_dict[full_state] = 1.0/len(ACTIONS[state_idx])

		return cls(policy_dict)

	# Construct policy by loading policy dictionary from file
	@classmethod
	def create_from_file(cls, filename):
		with open('obj/' + filename, 'rb') as f:
			return cls(pickle.load(f))

	### OTHER FUNCTIONALITY

	# Save the policy dictionary to file
	def save_to_file(self, filename):
		with open('obj/' + filename, 'wb') as f:
			pickle.dump(self.policy_function, f, pickle.HIGHEST_PROTOCOL)

	# Returns random action in current state according to policy
	def draw_action(self, current_state):
		is_same_suit = current_state[0]
		high_card = current_state[1]
		low_card = current_state[2]
		state = current_state[3]
		state_idx = STATES.index(state)
		u = random.uniform(0.0, 1.0)
		s = 0.0
		actions = ACTIONS[state_idx]
		for k in range(len(actions)):
			s += self.policy_function[(is_same_suit, high_card, low_card, state, actions[k])]
			if u < s:
				return actions[k]
	
	# Returns greedy action for current_state. If muliple actions are equal, one is picked randomly
	# This function is actually wrong. The "greedy action" is with respect to the state action
	# value function, not the policy function.
	def greedy_action(self, current_state):
		state = current_state[3]
		state_idx = STATES.index(state)
		actions = ACTIONS[state_idx]
		max_value_action = max(actions)
		optimal_idx = [i for i, j in enumerate(actions) if j == max_value_action]	
		return (current_state[0], current_state[1], current_state[2], state, actions[random.choice(optimal_idx)])

	# Updates policy in accordance with algorithm on p. 81 of [S&B 2018]
	def update(self, opt_state_action, epsilon = 0.01):
		is_same_suit = opt_state_action[0]
		high_card = opt_state_action[1]
		low_card = opt_state_action[2]
		state = opt_state_action[3]
		opt_action = opt_state_action[4]
		state_idx = STATES.index(state)
		for action in ACTIONS[state_idx]:
			if action == opt_action:
				self.policy_function[(is_same_suit, high_card, low_card, state, action)] = 1 - epsilon + epsilon/len(ACTIONS[state_idx])
			else:
				self.policy_function[(is_same_suit, high_card, low_card, state, action)] = epsilon/len(ACTIONS[state_idx])
# End of Policy class


# CLASS NAME: 	State_Action_Value_Function
#
# DESCRIPTION: 	This class defines a state action value function on the Game_State states
# 
# NOTES: 
#	Note 1 		- The state action value function is updated in accordance with the algorithm on p.
#				  81 of [S&B 2018], with one difference: Instead of averaging over all observations,
#				  a learning rate is used instead. This might work well since we can expect the
#				  the opponent's play style will change over time, and therefore convergence to a 
#				  stationary distribution is not desired.
#
# ref3

class State_Action_Value_Function:
	### CONSTRUCTORS

	def __init__(self, state_action_value_dict):
		self.state_action_value_function = state_action_value_dict

	# Construct uniform State_Action_Value_Function
	@classmethod
	def create_uniform(cls, init_value = 0.0):
		state_action_value_dict = {}
		for is_same_suit in range(2):
			for high_card in range(13):
				for low_card in range(13):
					for state_idx in range(len(STATES)):
						for action in ACTIONS[state_idx]:
							full_state = (is_same_suit, high_card, low_card, STATES[state_idx], action)
							state_action_value_dict[full_state] = init_value

		return cls(state_action_value_dict)

	# Construct State_Action_Value_Function by loading a dictionary from file
	@classmethod
	def create_from_file(cls, filename):
		with open('obj/' + filename, 'rb') as f:
			return cls(pickle.load(f))

	### OTHER FUNCTIONALITY

	# Save the policy dictionary to file
	def save_to_file(self, filename):
		with open('obj/' + filename, 'wb') as f:
			pickle.dump(self.state_action_value_function, f, pickle.HIGHEST_PROTOCOL)

	# Compute the greedy action with respect to state action value function
	def greedy_action(self, current_state):
		state = current_state[3]
		state_idx = STATES.index(state)
		actions = ACTIONS[state_idx]
		action_values = []
		for action_idx in range(len(actions)):
			action_values.append(self.state_action_value_function[(current_state[0], current_state[1], current_state[2], current_state[3], actions[action_idx])])
		max_action_value = max(action_values)
		optimal_action = []
		for idx in range(len(action_values)):
			if action_values[idx] == max_action_value:
				optimal_action.append(actions[idx])
		
		return (current_state[0], current_state[1], current_state[2], state, random.choice(optimal_action))
	
	# Updates state action value function. See Note 1.
	def update(self, state_action, payoff, learning_rate = 0.01):
		old_value = self.state_action_value_function[state_action]
		self.state_action_value_function[state_action] = learning_rate*payoff + (1.0 - learning_rate)*old_value
# End of State_Action_Value_Function


class Bot:
	def __init__(self, policy, state_action_value_function):
		self.policy = policy
		self.SAVF = state_action_value_function

	def take_action(self, current_state):
		pass
