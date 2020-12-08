"""
driver_user.py
Author: Teddy Rowan
Last Modified: December 3, 2020
Description: Driver function for user-created caffeine blood-concentration simulations. 

"""

from caffeine_levels import CaffeineLevels
import numpy as np
    

day_length = 15*60
pill_strength = 50

night_level = 20
optimal = 120


##pill_schedule = np.array([0, 60, 300]) #100mg pills
#pill_schedule = np.array([0, 1, 2, 120, 240, 360]) # 50mg pills
#pill_schedule = np.array([0, 1, 90, 230, 370]) # 50mg pills

#pill_schedule = np.array([0, 77, 306]) # 100mg (best to date)
#pill_schedule = np.array([0, 20, 21, 129, 285, 352]) # 50mg (best to date)
pill_schedule = np.array([0, 1, 2, 135, 240, 365]) # 50mg (user best)
optimal = 120

caff = CaffeineLevels(day_length, pill_strength, pill_schedule, optimal, night_level)
fit = caff.run_simulation()
print("Fitness: " + str(fit))
caff.plot_results()
