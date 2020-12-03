"""
caffeine_driver.py
Author: Teddy Rowan
Description: Driver function for caffeine blood-concentration simulations. 
"""

from caffeine_levels import CaffeineLevels
import numpy as np

day_length = 15*60
pill_strength = 100
pill_schedule = np.array([0, 60, 300])

caff = CaffeineLevels(day_length, pill_strength, pill_schedule)
caff.run_simulation()
