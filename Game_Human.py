"""
Michael Ramsey
Osman Malik
Erik Johnson
Kwan Ho Lee

Date Created: 04/01/18
Last Updated: 9/18/2018

This is a python script that runs a game of poker against a human player.
"""

# Import necessary packages
from deuces import Card
from deuces import Deck
from deuces import Evaluator
from Poker_Bot import Game_State
from Poker_Bot import Policy
from Poker_Bot import State_Action_Value_Function
import os

# Initialize game parameters
human_capital = 0.0
ai_capital = 0.0
gs = Game_State()
round_count = 1
learning_rate = 0.05
epsilon = 0.05
is_button = 1 # If AI is button

policy_suffix = ".policy"
savf_suffix = ".savf"
obj_path = "obj/"

bot_name = "bot_1" # Name of bot to play against. Will load existing bot or create new one.

# Load/create bot
if os.path.isfile(obj_path + bot_name + policy_suffix) and os.path.isfile(obj_path + bot_name + savf_suffix):
	print("Loading existing data for " + bot_name + "...")
	p = Policy.create_from_file(bot_name + policy_suffix)
	print("Loaded " + bot_name + " policy file")
	q = State_Action_Value_Function.create_from_file(bot_name + savf_suffix)
	print("Loaded " + bot_name + " state action value function file")
else:
	print("Policy and state action value function files don't exist for " + bot_name + ". Create new ones...")
	p = Policy.create_uniform()
	print("New policy function created for " + bot_name)
	q = State_Action_Value_Function.create_uniform()
	print("New policy function created for " + bot_name)

while True:
	# Start new round and deal cards
	print("Starting round " + str(round_count) + "...")
	gs.clear_state()
	deck = Deck()
	gs.set_player_cards(deck.draw(2))
	gs.set_opponent_cards(deck.draw(2))
	gs.set_flop(deck.draw(3))
	pot = 0.0
	if is_button:
		player_turn = 0
	else:
		player_turn = 1

	print('Your capital is: ' + str(human_capital))
	print('AIs capital is: ' + str(ai_capital))
	print('\nYour cards are: ')
	gs.print_opponent_cards()

	# Go through betting
	visited_action_states = []
	intermediate_payoffs = []
	human_fold_f = False # Flag for keeping track of if human has folded
	ai_fold_f = False # Flag for keeping track of if AI has folded
	raise_f = False # Flag for keeping track of if any subsequent "bets" are in fact raises 
	while gs.get_possible_actions():
		if player_turn == 0:
			print('\nPossible actions are: ' + str(gs.get_possible_actions()))
			action = raw_input('Make choice (just enter letter, e.g.: B): ')
			if action == 'B' and raise_f:
				pot += 2.0
				human_capital -= 2.0
			elif action == 'B' and not raise_f:
				pot += 1.0
				human_capital -= 1.0
				raise_f = True
			elif action == 'C':
				pot += 1.0
				human_capital -= 1.0
			elif action == 'F':
				human_fold_f = True
				break
			elif action == 'Ch':
				pass
		else:
			cs =  gs.get_current_state_id()
			action = p.draw_action(cs)
			print('AI takes action: ' + str(action))
			visited_action_states.append((cs[0], cs[1], cs[2], cs[3], action))
			if action == 'B' and raise_f:
				pot += 2.0
				ai_capital -= 2.0
				intermediate_payoffs.append(-2.0)
			elif action == 'B' and not raise_f:
				pot += 1.0
				ai_capital -= 1.0
				intermediate_payoffs.append(-1.0)
				raise_f = True
			elif action == 'C':
				pot += 1.0
				ai_capital -= 1.0
				intermediate_payoffs.append(-1.0)
			elif action == 'F':
				ai_fold_f = True
				intermediate_payoffs.append(0.0)
				break
			elif action == 'Ch':
				intermediate_payoffs.append(0.0)
		gs.append_action(action)
		print('The pot is: ' + str(pot))
		player_turn = (player_turn + 1) % 2
	is_button = (is_button + 1) % 2

	# Evaluate result and update the policy and state action value function
	print('AI hand is:')
	gs.print_player_cards()
	print('The flop is:')
	gs.print_flop()
	if human_fold_f:
		print('AI wins pot of size: ' + str(pot))
		intermediate_payoffs[-1] += pot
		ai_capital += pot
	elif ai_fold_f:
		print('Human wins pot of size: ' + str(pot))
		human_capital += pot
	elif gs.is_winner() == 1:
		print('AI wins pot of size: ' + str(pot))
		intermediate_payoffs[-1] += pot
		ai_capital += pot
	elif gs.is_winner() == -1:
		print('Human wins pot of size: ' + str(pot))
		human_capital += pot
	elif gs.is_winner() == 0:
		print('Draw')
		intermediate_payoffs[-1] += pot/2.0
		ai_capital += pot/2.0
		human_capital += pot/2.0
	round_count += 1
	G = 0
	for i, s in reversed(list(enumerate(visited_action_states))):
		G += intermediate_payoffs[i]
		q.update(s, G, learning_rate)
		greedy_action = q.greedy_action(visited_action_states[i])
		p.update(greedy_action, epsilon)

	# Ask if human wants to play another round, otherwise quit
	quit = raw_input('\nQuit? (Y/N) ')
	if quit == 'Y' or quit == 'y':
		break
	print('\n-----------------\n')
