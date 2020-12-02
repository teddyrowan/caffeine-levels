"""
caffeine_levels.py
Author: Teddy Rowan
Last Modified: December 2, 2020
Description: Numerical PDE simulation of caffeine levels in blood from taking caffeine pills.

TODO: clean up plots (legend, grid style, linestyle, figsize, etc.)
TODO: implement ML to optimize pill taking time.
        - I think for this we just say that the algo needs to figure out how to do four pills. 
            - Generate 50/100 random placements for the four pills. Then find profiles. Calculate fitness. 
            - Mutate and repeat. Identify the best profiles. 
        - I should turn this script into a class and then create a driver script to faciliate ML.

Notes: 
- Caffeine elimination half-life is 3-5 hours. [1]
    x^(3*60) = 0.50 ==> x ~ 0.99615658
    in seconds model: x ~ 0.9999358217
- Reaches peak-effects in 30-60 minutes. [1]
    Absorption half life ~ 15 mins? x^(15) = 0.50 ==> x ~ 0.9548416
    In seconds model: x ~ 0.9992301329
- Seconds model made no meaningful change and increased computation dramatically. 

[1] http://sleepeducation.org/news/2013/08/01/sleep-and-caffeine
"""

import matplotlib.pyplot as plt
import numpy as np

# Based on assumption of absorption half-life of 15 minutes
def caff_absorp(pill_remaining):
    return (1-0.9548416)*pill_remaining #minutes model
    #return (1-0.9992301329)*pill_remaining #seconds model

# Based on 180 steps for 3-hour half-life
def caff_depletion(blood_level):
    return (1-0.99615658)*blood_level #minutes model
    #return (1-0.9999358217)*blood_level #seconds model

# Create an optimal caffination profile.
def optimal_profile(time_list, optimal_caff, end_caff):
    fit = np.array([end_caff])
    for time in range(1, time_list.size):
        val = fit[time-1]/0.99615658
        if (val > optimal_caff):
            val = optimal_caff
        fit = np.append(fit, val)
    fit = np.flip(fit)
    return fit
    

## Main Start. 
time_list = np.array([])
pill_list = np.array([])
caff_list = np.array([])

pill_strength = 50;
# Strength of each caffeine pill (100 normal, 50 half, 5x20 for coffee)

caff_pill_level = caff_blood_level = 0
# Initial caffeine levels to start the day

time_awake = 16.5*60
# Assumes 8.30am to 1am = (3.5+12+1 hours)

time_step = 1
# How big of a step to take w/ each EM iteration

time_delay = 5
# How long in your stomach before the caffeine pill starts to break down and take effect.

#pill_time = np.array([0, 60, 300, 510]) + time_delay #100mg profile
pill_time = np.array([0, 1, 2, 120, 240, 360, 480]) + time_delay # 50mg pills # every 2hrs.

# Euler-Method step-through to solve profiles.
for seg in range(0, int(time_awake), time_step):
    time_list = np.append(time_list, seg)
    
    # If it's time to take a pill
    if (pill_time.size > 0 and seg == pill_time[0]):
        caff_pill_level = caff_pill_level + pill_strength
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
plt.title("Simualted Stomach-Caffeine Level")
plt.grid()
plt.show(block=False)

opt = optimal_profile(time_list, 120, 20)
# Calculate the ideal caffeine profile

fig = plt.figure()
plt.plot(time_list, caff_list, 'r-', markersize=1)
plt.plot(time_list, opt, 'b--')
plt.xlabel("Time since waking [minutes]")
plt.ylabel("Blood-caffeine level [mg]")
plt.title("Theoretical Blood-Caffeine Level")
plt.grid()
plt.show()