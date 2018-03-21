# Used to test stuff

from Poker_Bot import Game_State
from deuces import Card
from deuces import Deck
import numpy as np

gs = Game_State()
deck = Deck()
gs.set_player_cards(deck.draw(2))
gs.set_opponent_cards(deck.draw(2))
gs.set_flop(deck.draw(3))
gs.append_action('B')
gs.append_action('B')

gs.print_player_cards()
gs.print_opponent_cards()
gs.print_player_hand()
gs.print_opponent_hand()
print(gs.is_winner())
print gs.get_current_state_id()


# Used to test Policy class

from Poker_Bot import Policy
p = Policy.create_uniform()
opt_state_action = (1,2,4,('Ch','B'),'B')
p.update(opt_state_action)

# Used to test State_Action_Value_Function class

from Poker_Bot import State_Action_Value_Function
savf = State_Action_Value_Function.create_uniform(init_value = 0.0)

