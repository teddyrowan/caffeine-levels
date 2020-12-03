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

"""
To transfer:
pill_strength = 100 #50
time_awake = 16.5*60
pill_time = np.array([0, 60, 300]) + time_delay #100mg profile
pill_time = np.array([0, 1, 2, 120, 240, 360, 480]) + time_delay # 50mg pills # every 2hrs.
"""

import matplotlib.pyplot as plt
import numpy as np

class CaffeineLevels:
    
    def __init__(self, day_length, strength, pill_times):
        self.time_delay = 5
        # How long in your stomach before the caffeine pill starts to break down and take effect.

        self.pill_time = pill_times + self.time_delay
        self.time_awake = day_length
        self.pill_strength = strength
        self.time_step = 1

        
        self.caff_pill_level = self.caff_blood_level = 0
        # Initial caffeine levels to start the day
        
        self.time_list = np.array([])
        self.pill_list = np.array([])
        self.caff_list = np.array([])
        
        

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

        self.plot_results()

    def plot_results(self):
        fig = plt.figure()
        plt.plot(self.time_list, self.pill_list, 'r-', markersize=1)
        plt.xlabel("Time since waking [minutes]")
        plt.ylabel("Stomach-caffeine level [mg]")
        plt.title("Simualted Stomach-Caffeine Level")
        plt.grid()
        plt.show(block=False)

        self.opt = self.optimal_profile(self.time_list, 120, 20)
        # Calculate the ideal caffeine profile

        fig = plt.figure()
        plt.plot(self.time_list, self.caff_list, 'r-', markersize=1)
        plt.plot(self.time_list, self.opt, 'b--')
        plt.xlabel("Time since waking [minutes]")
        plt.ylabel("Blood-caffeine level [mg]")
        plt.title("Theoretical Blood-Caffeine Level")
        plt.grid()
        plt.show()
