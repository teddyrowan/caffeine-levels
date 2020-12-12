"""
driver_user.py
Author: Teddy Rowan
Last Modified: December 12, 2020
Description: Driver function for user-created caffeine blood-concentration simulations. 

"""

from caffeine_levels import CaffeineLevels
import numpy as np

pill_strength = 50
# What is the strength [mg] of the caffeine pills
    
day_length = 15*60
# How long is your day [minutes]

daytime_optimal = 120
# What is your optimal daytime caffeine level [mg]

night_level = 20
# What is your comfortable bedtime caffeine level [mg]

pill_schedule = np.array([0, 1, 2, 126, 238, 347])
# Best profile for 50mg pills (via ML) [times in minutes since waking]


""" 
Recommended pill schedules

pill_schedule = np.array([0, 1, 301])
# Best profile for 100mg pills (via ML)

pill_schedule = np.array([0, 1, 2, 126, 238, 347])
# Best profile for 50mg pills (via ML)

pill_schedule = np.array([0, 60, 300])
# Teddy's standard 100mg schedule
"""

# Initialize and run the simulation
caff = CaffeineLevels(day_length, pill_strength, pill_schedule, daytime_optimal, night_level)
fit = caff.run_simulation()
print("Fitness: " + str(fit))
caff.plot_stomach(False)
caff.plot_results()
