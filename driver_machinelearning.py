"""
driver_machinelearning.py
Author: Teddy Rowan
Last Modified: December 3, 2020
Description: Driver function for ML optimization of caffeine blood-concentration simulations. 

Current State:
- Mutation code is just not really improving sims a ton. 
    - I think it gets stuck with a value late in the schedule and then struggles to escape it
- Code also maybe is slow? Hard to tell. Should look at optimization.
"""

from caffeine_levels import CaffeineLevels
import numpy as np
import random

def generate_schedule(n_pills, max_time):
    sched = np.array([0]) #dope the schedule to take a pill at t=0
    
    while sched.size < n_pills:
        val = round(random.uniform(0, 1)*max_time)
        while val in sched:
            val = val + 1
        
        sched = np.append(sched, val)
    
    return np.sort(sched)

def mutate(old, comparison):
    new = np.array([])
    for index in range(0, old.size):
        val = round((2*old[index]+comparison[index]) / 3 + round(random.uniform(0, 1)*10) - 5)

        if (random.uniform(0,1) < 0.1): #1/10 chance, give something a totally new value
            val = round(random.uniform(0, 1)*day_length)

        # Make sure values are positive and unique.
        should_change = True
        val = val - 1
        while should_change:
            val = val + 1
            should_change = val in new
            if (not should_change):
                if (val < 0):
                    should_change = True
            
        new = np.append(new, val)     

    return new

# okay, do the ML Simulation.
day_length = 15*60
pill_strength = 100
optimal_caffeine = 120
night_caffeine = 20

population = 100
pill_count = 3

pop_arr = np.array([])

for ii in range(0, population):
    schedule = generate_schedule(pill_count, day_length)
    caff = CaffeineLevels(day_length, pill_strength, schedule, optimal_caffeine, night_caffeine)
    fit = caff.run_simulation()
    pop_arr = np.append(pop_arr, caff)

pop_arr = sorted(pop_arr, key=lambda x:x.fitness)
# Sort by fitness

print(pop_arr[0].pill_schedule)
# print the schedule for the best profile

print('Best Fitness: '+ str(pop_arr[0].fitness))
print('Median Fitness: '+ str(pop_arr[round(population/2)].fitness))
print('Worst Fitness: '+ str(pop_arr[-1].fitness))

pop_arr[0].plot_results()
# Plot the best fitness

#for entry in pop_arr:
#    print(entry.fitness)

# save the top 5, iterate through the rest w/ probability fitness[x]/fitness[-1] of mutating
# if mutating: randomly choose one from top 25%, take the avg value for each data point, then add a random change to it
for jj in range(5, population):
    if (random.uniform(0,1) < pop_arr[jj].fitness/pop_arr[-1].fitness):
        transform_index = round(random.uniform(0,1)*population*0.25)
        
        new_sched = mutate(pop_arr[jj].pill_schedule, pop_arr[transform_index].pill_schedule)
        pop_arr[jj].pill_schedule = new_sched

counter = 1
while (counter < 100):
    print('Repeating for ' + str(counter) + ' gen.')
    counter = counter + 1
    
    pop_arr2 = np.array([])
    for ii in range(0, population):
        caff = CaffeineLevels(day_length, pill_strength, pop_arr[ii].pill_schedule, optimal_caffeine, night_caffeine)
        fit = caff.run_simulation()
        pop_arr2 = np.append(pop_arr2, caff)
    
    pop_arr2 = sorted(pop_arr2, key=lambda x:x.fitness)


    print(pop_arr2[0].pill_schedule)
    # print the schedule for the best profile

    print('Best Fitness: '+ str(pop_arr2[0].fitness))
    print('Median Fitness: '+ str(pop_arr2[round(population/2)].fitness))
    print('Worst Fitness: '+ str(pop_arr2[-1].fitness))

    if not (counter % 20):
        pop_arr2[0].plot_results()

    for jj in range(5, population):
        if (random.uniform(0,1) < pop_arr2[jj].fitness/pop_arr2[-1].fitness):
            transform_index = round(random.uniform(0,1)*population*0.25)
            new_sched = mutate(pop_arr2[jj].pill_schedule, pop_arr2[transform_index].pill_schedule)
            pop_arr2[jj].pill_schedule = new_sched
    
    pop_arr = pop_arr2