"""
settings_ml.py
Author: Teddy Rowan
Last Modified: December 12, 2020
Description: Settings for the machine-learning driver function for the caffeine simulations.
"""

def get_settings():
    settings = {}

    settings['day_length'] = 15*60
    # Common: [15*60, ((12-8.5)+12+0.5)*60 = 16*60]
    
    settings['pill_strength'] = 100
    # Common: 50mg, 100mg
    
    settings['pill_count'] = 3
    # How many pills/half-pills to take
    
    settings['optimal_caffeine'] = 120
    # Desired caffeine during daytime hours [mg]
    
    settings['night_caffeine'] = 20
    # Acceptable caffeine level at bedtime [mg]
        
    settings['population'] = 250
    # How many sims in each generation
    
    settings['generations'] = 50
    # How many generations of simulations to run
    
    settings['alpha'] = 0.08
    # Visibility of all the populations on the plots
    # 0.08 for 250 pop, 0.03 for 2500/5000
    
    return settings