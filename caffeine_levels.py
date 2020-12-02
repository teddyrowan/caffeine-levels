"""
caffeine_levels.py
Author: Teddy Rowan
Last Modified: December 1, 2020
Description: Numerical PDE simulation of caffeine levels in blood from taking caffeine pills.

TODO: define constants (time, caffeine pill values, time_delay, etc.)
TODO: extend simulation to model cup of coffee.
TODO: implement ML to optimize pill taking time.

Notes: 
- Caffeine elimination half-life is 3-5 hours. [1]
    x^(3*60) = 0.50 ==> x ~ 0.99615658
- Reaches peak-effects in 30-60 minutes. [1]
    Absorption half life ~ 15 mins? x^(15) = 0.50 ==> x ~ 0.9548416

[1] http://sleepeducation.org/news/2013/08/01/sleep-and-caffeine
"""


import matplotlib.pyplot as plt
import numpy as np

# Based on assumption of absorption half-life of 15 minutes
def caff_absorp(pill_remaining):
    return (1-0.9548416)*pill_remaining

# Based on 180 steps for 3-hour half-life
def caff_depletion(blood_level):
    return (1-0.99615658)*blood_level

## Main Start. 
time_list = np.array([])
pill_list = np.array([])
caff_list = np.array([])

time_delay = 5
pill_time = np.array([0, 60, 300, 500]) + time_delay

time_wake = 0 
time_sleep = 16.5*60
# Assumes 8.30am to 1am = (3.5+12+1 hours)

time_step = 1

caff_pill_level = 0
# Initial caffeine level in stomach

caff_blood_level = 0
# Initial caffeine level in bloodstream

for seg in range(time_wake, int(time_sleep), time_step):
    time_list = np.append(time_list, seg)
    
    # If it's time to take a pill
    if (pill_time.size > 0 and seg == pill_time[0]):
        caff_pill_level = caff_pill_level + 100
        pill_time = np.delete(pill_time, 0)
    
    caff_depl = caff_depletion(caff_blood_level)
    caff_absp = caff_absorp(caff_pill_level)
    
    caff_pill_level = caff_pill_level - caff_absp
    caff_blood_level = caff_blood_level + caff_absp - caff_depl

    pill_list = np.append(pill_list, caff_pill_level)
    caff_list = np.append(caff_list, caff_blood_level)
    

fig = plt.figure()
plt.plot(time_list, pill_list, 'r-', markersize=1)
plt.xlabel("Time since waking [minutes]")
plt.ylabel("Stomach-caffeine level [mg]")
plt.title("Stomach-Caffeine Simulation")
plt.grid()
plt.show(block=False)

fig = plt.figure()
plt.plot(time_list, caff_list, 'r-', markersize=1)
plt.xlabel("Time since waking [minutes]")
plt.ylabel("Blood-caffeine level [mg]")
plt.title("Blood-Caffeine Simulation")
plt.grid()
plt.show()