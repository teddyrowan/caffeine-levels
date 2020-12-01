"""
caffeine_levels.py
Author: Teddy Rowan
Last Modified: December 1, 2020
Description: Numerical PDE simulation of caffeine levels in blood from taking caffeine pills.
"""

import matplotlib.pyplot as plt
import numpy as np

time_list = np.array([])
pill_list = np.array([])
caff_list = np.array([])

time_wake = 0 
# Assume 9am for now

time_sleep = 15*60 
# Assume midnight for now

time_step = 1

for seg in range(time_wake, time_sleep, time_step):
    # Do calculations here. to solve value to add to pill_list and caff_list
    
    time_list = np.append(time_list, seg)
    pill_list = np.append(pill_list, 1)
    caff_list = np.append(caff_list, 2*seg)
    

fig = plt.figure()
plt.plot(time_list, caff_list, 'ro-', markersize=3)
plt.xlabel("Time since waking [minutes]")
plt.ylabel("Caffeine Level")
plt.title("Blood-caffeine simulated levels [mg]")
plt.grid()
plt.show()