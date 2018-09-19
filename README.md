# CSCI_5622_project
We use reinforcement learning methods to train a bot how to play fixed-limit texas hold-em.

## Files
Create_policy: Python script to create a policy for a poker bot (how the bot plays).

Game_Human: Python script that allows a human to play poker against an instance of a bot.

Game_Train_Itself: Python script to train a poker bot against another instance of itself.

Game_Train_Itself_Predet: Python script to train a poker bot aginst a bot that has a set strategy. We essentilly just delete the policy update for the second bot in "Game_Train_Itself.py".

Poker_Bot: Python file to store Poker_Bot module.

SAVF_Visualization: Python file to visualize the SAVF as the bot trains over time.

Test_Learning: Python file that records accumulated winnings of a bot that is being trained against a bot with a set strategy.

test_script: Python script for testing Poker_Bot module.

## Folders
Accumulated_Winnings: Contains plots and a python script to track the accumulated winnings of the bot.

deuces: Python module developed for printing nice playing cards. Taken from: https://github.com/worldveil/deuces.

old_code: Old code.

SAVF_Plots: Plots of the State Action Value Function.
