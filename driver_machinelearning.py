"""
driver_machinelearning.py
Author: Teddy Rowan
Last Modified: December 3, 2020
Description: Driver function for ML optimization of caffeine blood-concentration simulations. 

TODO: only print shit when there is a change in the new-best
TODO: mutation code just isn't good.
    Keep top 5% of sims.
        - Let's say 10% chance of totally new sim
        - 40% chance of modifying current values
            - 50% chance to move each value -10 to 10 mins from current
        - 50% chance of taking one of the best 10% of current sims and modifying. 
            - 50% chance of moving each value from -10 to 10 mins of current.
            - 25% chance of entirely new value
            - 25% chance of no change.
    Sort new schedule before returning. 
"""

from caffeine_levels import CaffeineLevels
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_schedule(n_pills, max_time):
    sched = np.array([0]) # dope the schedule to take a pill at t=0
    
    while sched.size < n_pills:
        val = round(random.uniform(0, 1)*max_time)
        while val in sched:
            val = val + 1
        
        sched = np.append(sched, val)
    
    return np.sort(sched)

def mutate(old, comparison):
    new = np.array([])
    for index in range(0, old.size):
        #val = round((2*old[index]+comparison[index]) / 3 + round(random.uniform(0, 1)*10) - 5)
        
        dna_frac = random.uniform(0,1)
        rand_add = random.uniform(0, 1)*10 - 5
        val = round((old[index]*dna_frac + comparison[index]*(1-dna_frac)) + rand_add)
        

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

def print_fitness(arr, pop_size):
    print('Best Fitness: '+ str(arr[0].fitness))
    print('Median Fitness: '+ str(arr[round(pop_size/2)].fitness))
    print('Worst Fitness: '+ str(arr[-1].fitness))
    
def plot_all(data):
    fig = plt.subplots()
    for sim in data:
        blood = plt.plot(sim.time_list, sim.caff_list, 'r-', alpha=0.08)
    
    plt.plot(data[0].time_list, data[0].caff_list, 'b-')
    plt.plot(sim.time_list, sim.opt, 'g-')
    
    
    plt.xlabel("Time since waking [minutes]")
    plt.ylabel("Blood-caffeine level [mg]")
    plt.title("Blood-Caffeine Simulation")
    plt.xlim([0, day_length])
    plt.ylim([0, 165])
            
    plt.grid()
    plt.show()
    


# okay, do the ML Simulation.
day_length = 15*60 #((12-8.5) + (12) + 0.5)*60 #16hrs
pill_strength = 100#50#100
optimal_caffeine = 120
night_caffeine = 20

population = 100#250
pill_count = 3#6#3

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

print_fitness(pop_arr, population)
# Print best/worst/median fitness values

#pop_arr[0].plot_results()
# Plot the best fitness

plot_all(pop_arr)
#exit()

# save the top 5, iterate through the rest w/ probability fitness[x]/fitness[-1] of mutating
# if mutating: randomly choose one from top 25%, take the avg value for each data point, then add a random change to it
for jj in range(5, population):
    if (random.uniform(0,1) < pop_arr[jj].fitness/pop_arr[-1].fitness):
        transform_index = round(random.uniform(0,1)*population*0.25)
        
        new_sched = mutate(pop_arr[jj].pill_schedule, pop_arr[transform_index].pill_schedule)
        pop_arr[jj].pill_schedule = new_sched

counter = 1
while (counter < 101):
    print('Repeating for gen: ' + str(counter))
    counter = counter + 1
    
    pop_arr2 = np.array([])
    for ii in range(0, population):
        caff = CaffeineLevels(day_length, pill_strength, pop_arr[ii].pill_schedule, optimal_caffeine, night_caffeine)
        fit = caff.run_simulation()
        pop_arr2 = np.append(pop_arr2, caff)
    
    pop_arr2 = sorted(pop_arr2, key=lambda x:x.fitness)

    #TODO: only print if it's a new schedule. 
    print(pop_arr2[0].pill_schedule)
    # Print the schedule for the best profile

    print_fitness(pop_arr2, population)
    # Print best/worst/median fitness values

    if not (counter % 20):
        plot_all(pop_arr2)
        #pop_arr2[0].plot_results()

    for jj in range(5, population):
        if (random.uniform(0,1) < pop_arr2[jj].fitness/pop_arr2[-1].fitness):
            transform_index = round(random.uniform(0,1)*population*0.25)
            new_sched = mutate(pop_arr2[jj].pill_schedule, pop_arr2[transform_index].pill_schedule)
            pop_arr2[jj].pill_schedule = new_sched
    
    pop_arr = pop_arr2