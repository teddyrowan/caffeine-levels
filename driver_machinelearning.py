"""
driver_machinelearning.py
Author: Teddy Rowan
Last Modified: December 10, 2020
Description: Driver function for ML optimization of caffeine blood-concentration simulations. 

TODO: abstract helper code to another file.
TODO: abstract mutation code.
TODO: mutation code just isn't good. (better-ish now??)
    Keep top 5% of sims.
        - 10% chance of totally new sim
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
import settings_ml as sml

def generate_schedule(n_pills, max_time):
    #sched = np.array([0]) # dope the schedule to take a pill at t=0
    sched = np.array([]) # no doping
    
    while sched.size < n_pills:
        val = round(random.uniform(0, 1)*max_time)
        while val in sched: # avoid duplicates
            val = val + 1
        
        sched = np.append(sched, val)
    
    return np.sort(sched)

def mutate(old, comparison):
    new = np.array([])
    for index in range(0, old.size):
        dna_frac = random.uniform(0,0.5) # can't keep more than half of bad DNA
        rand_add = random.uniform(0, 1)*20 - 10
        val = round((old[index]*dna_frac + comparison[index]*(1-dna_frac)) + rand_add)
        
        if (random.uniform(0,1) < 0.1): #1/10 chance, give something a totally new value
            val = round(random.uniform(0, 1)*settings['day_length'])

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

    return np.sort(new)

def print_fitness(arr, pop_size, print_all):
    print('Best Fitness: '+ str(arr[0].fitness))
    if (print_all):
        print('Median Fitness: '+ str(arr[round(pop_size/2)].fitness))
        print('Worst Fitness: '+ str(arr[-1].fitness))
    
# TODO: add legend
def plot_all(data, gen, display):
    plt.rcParams['figure.figsize'] = (8, 5)
    fig = plt.figure()

    for sim in data:
        blood = plt.plot(sim.time_list, sim.caff_list, 'r-', alpha=settings['alpha']) #0.08 for 250pop

    aa = plt.plot(data[0].time_list, data[0].caff_list, 'b-', linewidth=2)
    bb = plt.plot(sim.time_list, sim.opt, 'g--', linewidth=2)
    
    plt.xlabel("Time since waking [minutes]")
    plt.ylabel("Blood-caffeine level [mg]")
    plt.title("Blood-Caffeine Simulation. Gen: [" + str(gen) + "]")
    plt.xlim([0, settings['day_length']])
    plt.ylim([0, 165])
            
    plt.grid()
    name = "r" + "{:03d}".format(gen) + "_blood.png"
    plt.savefig('./screens/' + name)
    if (display):
        plt.show()
   
    # Fix memory issues
    fig.clear()
    plt.close(fig)
    del aa
    del bb
    del blood


settings = sml.get_settings()
pop_arr = np.array([])

for ii in range(0, settings['population']):
    schedule = generate_schedule(settings['pill_count'], settings['day_length'])
    caff = CaffeineLevels(settings['day_length'], settings['pill_strength'], schedule, settings['optimal_caffeine'], settings['night_caffeine'])
    fit = caff.run_simulation()
    pop_arr = np.append(pop_arr, caff)

pop_arr = sorted(pop_arr, key=lambda x:x.fitness)
# Sort by fitness

print(pop_arr[0].pill_schedule)
# Print the schedule for the best profile

print_fitness(pop_arr, settings['population'], False)
# Print best/worst/median fitness values

plot_all(pop_arr, 0, False)

# save the top 5, iterate through the rest w/ probability fitness[x]/fitness[-1] of mutating
# if mutating: randomly choose one from top 25%, take the avg value for each data point, then add a random change to it
for jj in range(5, settings['population']):
    if (random.uniform(0,1) < pop_arr[jj].fitness/pop_arr[-1].fitness):
        transform_index = round(random.uniform(0,1)*settings['population']*0.25)
        new_sched = mutate(pop_arr[jj].pill_schedule, pop_arr[transform_index].pill_schedule)
        pop_arr[jj].pill_schedule = new_sched

sched = pop_arr[0].pill_schedule
for counter in range(1,settings['generations']+1):
    print('Repeating for gen: ' + str(counter))
    
    pop_arr2 = np.array([])
    for ii in range(0, settings['population']):
        caff = CaffeineLevels(settings['day_length'], settings['pill_strength'], pop_arr[ii].pill_schedule, settings['optimal_caffeine'], settings['night_caffeine'])
        fit = caff.run_simulation()
        pop_arr2 = np.append(pop_arr2, caff)
    
    pop_arr2 = sorted(pop_arr2, key=lambda x:x.fitness)

    # Print the schedule for the best profile if it's new
    if (not np.array_equal(sched, pop_arr2[0].pill_schedule)):
        sched = pop_arr2[0].pill_schedule        
        print(pop_arr2[0].pill_schedule)
        print_fitness(pop_arr2, settings['population'], False)

    plot_all(pop_arr2, counter, False)
    
    # Mutate the data
    for jj in range(5, settings['population']):
        if (random.uniform(0,0.8) < pop_arr2[jj].fitness/pop_arr2[-1].fitness):
            transform_index = round(random.uniform(0,1)*settings['population']*0.10)
            new_sched = mutate(pop_arr2[jj].pill_schedule, pop_arr2[transform_index].pill_schedule)
            pop_arr2[jj].pill_schedule = new_sched
    
    pop_arr = pop_arr2