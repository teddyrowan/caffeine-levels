"""
caffeine_levels.py
Author: Teddy Rowan
Last Modified: December 1, 2020
Description: Numerical PDE simulation of caffeine levels in blood from taking caffeine pills.

TODO: implement caffeine absorption function
TODO: implement caffeine depletion function
TODO: implement a list of caffeine pill taking times + adjustments for when to increase levels

"""


import matplotlib.pyplot as plt
import numpy as np

# Just quick assume 1/100th absorbed per interval
def caff_absorp(pill_remaining):
    # TODO: implement this properly
    return pill_remaining/10

def caff_depletion(blood_level):
    # TODO: implement this properly
    return blood_level/100

## Main Start. 
time_list = np.array([])
pill_list = np.array([])
caff_list = np.array([])

#TODO: create a time_intake list for when pills are taken. 

time_wake = 0 
# Assume 9am for now

time_sleep = 15*60 
# Assume midnight for now

time_step = 1

caff_pill_level = 100
# Initial caffeine level in stomach

caff_blood_level = 0
# Initial caffeine level in bloodstream

for seg in range(time_wake, time_sleep, time_step):
    time_list = np.append(time_list, seg)
    
    caff_depl = caff_depletion(caff_blood_level)
    caff_absp = caff_absorp(caff_pill_level)
    
    caff_pill_level = caff_pill_level - caff_absp
    caff_blood_level = caff_blood_level + caff_absp - caff_depl

    # Do calculations here. to solve value to add to pill_list and caff_list
    pill_list = np.append(pill_list, caff_pill_level)
    caff_list = np.append(caff_list, caff_blood_level)
    

fig = plt.figure()
plt.plot(time_list, pill_list, 'ro-', markersize=3)
plt.xlabel("Time since waking [minutes]")
plt.ylabel("Stomach-caffeine level [mg]")
plt.title("Stomach-Caffeine Simulation")
plt.grid()
plt.show(block=False)

fig = plt.figure()
plt.plot(time_list, caff_list, 'ro-', markersize=3)
plt.xlabel("Time since waking [minutes]")
plt.ylabel("Blood-caffeine level [mg]")
plt.title("Blood-Caffeine Simulation")
plt.grid()
plt.show()