"""
caffeine_levels.py
Author: Teddy Rowan
Last Modified: December 3, 2020
Description: Numerical PDE simulation (Euler-Method) of caffeine levels in blood from taking caffeine pills.

TODO: clean up plots (grid style, linestyle, figsize, etc.)

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

class CaffeineLevels:
    
    def __init__(self, day_length, strength, pill_times, optimal, night_level):
        self.time_delay = 5
        # How long in your stomach before the caffeine pill starts to break down and take effect.

        self.pill_time = pill_times + self.time_delay
        self.time_awake = day_length
        self.pill_strength = strength
        self.optimal_level = optimal
        self.night_level = night_level
        
        self.time_step = 1
        
        
        self.caff_pill_level = self.caff_blood_level = 0
        # Initial caffeine levels to start the day
        
        self.time_list = np.array([])
        self.pill_list = np.array([])
        self.caff_list = np.array([])
        
        self.pill_schedule = pill_times
        # Make a copy of the schedule

    # Based on assumption of absorption half-life of 15 minutes
    def _caff_absorp(self, pill_remaining):
        return (1-0.9548416)*pill_remaining #minutes model

    # Based on 180 steps for 3-hour half-life
    def _caff_depletion(self, blood_level):
        return (1-0.99615658)*blood_level #minutes model
    
    # Create an optimal caffination profile.
    def optimal_profile(self, time_list, optimal_caff, end_caff):
        fit = np.array([end_caff])
        for time in range(1, time_list.size):
            val = fit[time-1]/0.99615658
            if (val > optimal_caff):
                val = optimal_caff
            fit = np.append(fit, val)

        fit = np.flip(fit)
        return fit
    
    
    def run_simulation(self):
        # Euler-Method step-through to solve profiles.
        for seg in range(0, int(self.time_awake), self.time_step):
            self.time_list = np.append(self.time_list, seg)
    
            # If it's time to take a pill
            if (self.pill_time.size > 0 and seg == self.pill_time[0]):
                self.caff_pill_level = self.caff_pill_level + self.pill_strength
                self.pill_time = np.delete(self.pill_time, 0)
    
            self.caff_depl = self._caff_depletion(self.caff_blood_level)
            self.caff_absp = self._caff_absorp(self.caff_pill_level)
    
            self.caff_pill_level = self.caff_pill_level - self.caff_absp
            self.caff_blood_level = self.caff_blood_level + self.caff_absp - self.caff_depl

            self.pill_list = np.append(self.pill_list, self.caff_pill_level)
            self.caff_list = np.append(self.caff_list, self.caff_blood_level)

        self.opt = self.optimal_profile(self.time_list, self.optimal_level, self.night_level)
        # Calculate the ideal caffeine profile

        return self.calculate_fitness()

    # Fitness defined as sum of squares of difference between blood-caffeine and optimal-profile.
    # Lower is better. 
    def calculate_fitness(self):
        sum = 0;
        for step in range(0, self.time_list.size):
            sum = sum + pow(self.caff_list[step] - self.opt[step], 2)
            if (self.opt[step] < self.optimal_level+1 and self.caff_list[step] > self.opt[step]):
                # If it's going to effect bedtime caffeine levels, double the fitness deviation.
                sum = sum + 1000*pow(self.caff_list[step] - self.opt[step], 2)
        
        self.fitness = sum
        return self.fitness
        

    def plot_results(self):
        fig = plt.figure()
        plt.plot(self.time_list, self.pill_list, 'r-', markersize=1)
        plt.xlabel("Time since waking [minutes]")
        plt.ylabel("Stomach-caffeine level [mg]")
        plt.title("Simualted Stomach-Caffeine Level")
        plt.grid()
        plt.show(block=False)

        fig = plt.subplots()
        ideal = plt.plot(self.time_list, self.opt, 'b--', label = 'Goal blood-caffeine')
        blood = plt.plot(self.time_list, self.caff_list, 'r-', label='Theorectical blood-caffeine')
        plt.xlabel("Time since waking [minutes]")
        plt.ylabel("Blood-caffeine level [mg]")
        plt.title("Blood-Caffeine Simulation")
        
        plt.legend()
                
        plt.grid()
        plt.show()
