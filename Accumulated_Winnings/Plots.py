"""
Michael Ramsey
Osman Malik
Erik Johnson
Kwan Ho Lee

Date Created: 04/01/18
Last Updated: 9/18/2018

This is a python script that plots the accumulated winnings dictionary file for the
desired poker bot.
"""

# Import necessary packages
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Arial', 'size':'34', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 'size':'24'}

# Set the font properties (for use in legend)
font_path = 'C:\Windows\Fonts\Arial.ttf'
font_prop = font_manager.FontProperties(fname=font_path, size=14)

# Plot the results
N = 19000000
plt.figure(figsize=(14,8)) # Control figure size
ax = plt.subplot() # Defines ax variable by creating an empty plot
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(20)
with open('acc_win1.p', 'rb') as file:
    data = pickle.load(file)
    sum1 = np.cumsum(data)
    plt.plot(sum1[0:N], label='epsilon = 0.00')
with open('acc_win2.p', 'rb') as file:
    data = pickle.load(file)
    sum1 = np.cumsum(data)
    plt.plot(sum1[0:N], label='epsilon = 0.05')
with open('acc_win3.p', 'rb') as file:
    data = pickle.load(file)
    sum1 = np.cumsum(data)
    plt.plot(sum1[0:N], label='epsilon = 0.10')
with open('acc_win4.p', 'rb') as file:
    data = pickle.load(file)
    sum1 = np.cumsum(data)
    plt.plot(sum1[0:N], label='epsilon = 0.20')
plt.title('Accumulated winnings for different epsilon with SAVF = 0',**title_font)
plt.xlabel('Number of hands',**axis_font)
plt.ylabel('Accumulated winnings',**axis_font)
plt.legend(loc='lower right',prop=font_prop, numpoints=1)
plt.savefig("SAVF0_eps_New")
plt.show()