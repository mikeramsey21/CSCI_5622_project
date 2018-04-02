# Load the necessary packages
from deuces import Card
from deuces import Deck
from deuces import Evaluator
from Poker_Bot import Game_State
from Poker_Bot import Policy
from Poker_Bot import State_Action_Value_Function
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt

# The suffixes needed to load the dictionary files
policy_suffix = ".policy"
savf_suffix = ".savf"

# Parameters
bot_name = "bot_46_ep2_lr001" # The bot that you want to view
obj_path = "snaps/"  # The folder that your bot is in
tot_snap = 36       # The total number of bot snapshots

# Initialize matrices to stor2 information
prob_bet = np.zeros((tot_snap,10))
prob_fold = np.zeros((tot_snap,10))
savf_bet = np.zeros((tot_snap,10))
savf_fold = np.zeros((tot_snap,10))


count = 0
for i in range(0,tot_snap):

    # Load the policies
    p = Policy.create_from_file(obj_path + bot_name + '_sh' + str(100000*(i+1)) +  policy_suffix)
    q = State_Action_Value_Function.create_from_file(obj_path + bot_name + '_sh' + str(100000*(i+1)) + savf_suffix)

    # Convert the policies to dictionaries
    policy = p.policy_function
    savf = q.state_action_value_function

    # The cards that we are interested in tracking
    # Ace, Ace
    prob_bet[i][0] = policy[(0,12,12,(),'B')]
    prob_fold[i][0] = policy[(0,12,12,('B',),'F')]
    savf_bet[i][0] = savf[(0,12,12,(),'B')]
    savf_fold[i][0] = savf[(0,12,12,('B',),'F')]

    # Ace, King suited
    prob_bet[i][1] = policy[(1,12,11,(),'B')]
    prob_fold[i][1] = policy[(1,12,11,('B',),'F')]
    savf_bet[i][1] = savf[(1,12,11,(),'B')]
    savf_fold[i][1] = savf[(1,12,11,('B',),'F')]

    # Oueen, Jack suited
    prob_bet[i][2] = policy[(1,11,10,(),'B')]
    prob_fold[i][2] = policy[(1,11,10,('B',),'F')]
    savf_bet[i][2] = savf[(1,11,10,(),'B')]
    savf_fold[i][2] = savf[(1,11,10,('B',),'F')]

    # Queen, Jack off-suite
    prob_bet[i][3] = policy[(0,11,10,(),'B')]
    prob_fold[i][3] = policy[(0,11,10,('B',),'F')]
    savf_bet[i][3] = savf[(0,11,10,(),'B')]
    savf_fold[i][3] = savf[(0,11,10,('B',),'F')]

    # Ace, Eight off-suite
    prob_bet[i][4] = policy[(0,12,6,(),'B')]
    prob_fold[i][4] = policy[(0,12,6,('B',),'F')]
    savf_bet[i][4] = savf[(0,12,6,(),'B')]
    savf_fold[i][4] = savf[(0,12,6,('B',),'F')]

    # Five, Six off-suite
    prob_bet[i][5] = policy[(0,4,3,(),'B')]
    prob_fold[i][5] = policy[(0,4,3,('B',),'F')]
    savf_bet[i][5] = savf[(0,4,3,(),'B')]
    savf_fold[i][5] = savf[(0,4,3,('B',),'F')]

    # Seven, Seven
    prob_bet[i][6] = policy[(0,5,5,(),'B')]
    prob_fold[i][6] = policy[(0,5,5,('B',),'F')]
    savf_bet[i][6] = savf[(0,5,5,(),'B')]
    savf_fold[i][6] = savf[(0,5,5,('B',),'F')]

    # Two, Two
    prob_bet[i][7] = policy[(0, 0, 0, (), 'B')]
    prob_fold[i][7] = policy[(0, 0, 0, ('B',), 'F')]
    savf_bet[i][7] = savf[(0, 0, 0, (), 'B')]
    savf_fold[i][7] = savf[(0, 0, 0, ('B',), 'F')]

    # Two, Seven suited
    prob_bet[i][8] = policy[(1, 5, 0, (), 'B')]
    prob_fold[i][8] = policy[(1, 5, 0, ('B',), 'F')]
    savf_bet[i][8] = savf[(1, 5, 0, (), 'B')]
    savf_fold[i][8] = savf[(1, 5, 0, ('B',), 'F')]

    # Two, Seven off-suite
    prob_bet[i][9] = policy[(0, 5, 0, (), 'B')]
    prob_fold[i][9] = policy[(0, 5, 0, ('B',), 'F')]
    savf_bet[i][9] = savf[(0, 5, 0, (), 'B')]
    savf_fold[i][9] = savf[(0, 5, 0, ('B',), 'F')]

# Look at the policy function
print("The betting probability")
print("AA, AKS, QJs, QJ, A8, 56, 77, 22, 72s, 72")
print(prob_bet)

print("The folding probability")
print("AA, AKS, QJs, QJ, A8, 56, 77, 22, 72s, 72")
print(prob_fold)

# Look at the state action value function
print("The betting SAVF")
print("AA, AKS, QJs, QJ, A8, 56, 77, 22, 72s, 72")
print(savf_bet)

print("The folding SAVF")
print("AA, AKS, QJs, QJ, A8, 56, 77, 22, 72s, 72")
print(savf_fold)

# Plot some stuff
no_plot_col = 4
no_plot_row = 3
titles = ['AA', 'AKs', 'QJs', 'QJ', 'A8', '56', '77', '22', '72s', '72']
fig, axes = plt.subplots(no_plot_row, no_plot_col)
for fidx in range(0,10):
	axes[fidx/no_plot_col, fidx%no_plot_col].plot(savf_bet[:,fidx])
	axes[fidx/no_plot_col, fidx%no_plot_col].set_title(titles[fidx])
	axes[fidx/no_plot_col, fidx%no_plot_col].grid()
plt.show()
