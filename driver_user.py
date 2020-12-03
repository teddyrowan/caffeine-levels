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
##pill_schedule = np.array([0, 60, 300]) #100mg pills
pill_schedule = np.array([0, 1, 2, 120, 240, 360]) # 50mg pills

caff = CaffeineLevels(day_length, pill_strength, pill_schedule)
fit = caff.run_simulation()
caff.plot_results()
