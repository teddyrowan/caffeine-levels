"""
driver_machinelearning.py
Author: Teddy Rowan
Last Modified: December 3, 2020
Description: Driver function for ML optiomization of caffeine blood-concentration simulations. 

TODO: save the best couple of children and mutate the rest of the population

"""

from caffeine_levels import CaffeineLevels
import numpy as np
import random

def generate_schedule(n_pills, max_time):
    sched = np.array([0]) #dope the schedule to take a pill at t=0
    
    while sched.size < n_pills:
        val = round(random.uniform(0, 1)*max_time)
        sched = np.unique(np.append(sched, val)) #only add the value if it's unique
    
    return np.sort(sched)
    
    

# okay lets do the ML simulation
# start with 50mg pills. 100mg is boring b/c it's just randomly choosing 2 pills. 

day_length = 15*60
pill_strength = 100

population = 100
pill_count = 3

pop_arr = np.array([])

for ii in range(0, population):
    schedule = generate_schedule(pill_count, day_length)
    caff = CaffeineLevels(day_length, pill_strength, schedule)
    fit = caff.run_simulation()
    pop_arr = np.append(pop_arr, caff)

pop_arr = sorted(pop_arr, key=lambda x:x.fitness)
# Sort by fitness

print(pop_arr[0].pill_schedule)
# print the schedule for the best profile

pop_arr[0].plot_results()
# Plot the best fitness

