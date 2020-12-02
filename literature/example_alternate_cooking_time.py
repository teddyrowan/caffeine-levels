"""
alternate_cooking_time.py (python3)
Author: Teddy Rowan
Last Modified: July 19, 2020
Description: Numerical PDE solver to calculate alternative cooking times (based on total heat transfer) for different oven temperatures.

TODO: root solve from c1 approximation to find a better approximation using known cooking time as gauge. 

Example Inputs (Frozen Chicken Strips):
    type: c             # celcius
    temp_init  = -15    # 258 K Initial Chicken Temperature
    temp_final =  75    # 348 K Final Chicken Tmeperature
    oven_rec   = 215    # 488 K Hot version of the oven
    time_rec   = 20     # original cooking time [20 minutes]
    oven_new   = 150    # 423 K Cold version of the oven
"""
import matplotlib.pyplot as plt
import numpy as np

# Takes in the intial and final temperatures of the food, the original oven settings, the original cooking time, and the new oven settings and calculates cooking time based on the new settings. All temperatures in Kelvin. Output [time] in the same units as time input.
def calculate_cook_time(start_temp, end_temp, hot_oven_temp, cold_oven_temp, original_time):
    if cold_oven_temp < end_temp:
        print("WARNING: The new cooking temperature is too low to cook the food"); exit()
    if end_temp < start_temp:
        print("WARNING: Ovens heat food, don't cool them. Check your inputs."); exit()
    if original_time <= 0:
        print("WARNING: Ovens are not time machines."); exit()
    
    step_precision = 100 # how many steps to use in c1 approximation
    c1 = (end_temp-start_temp)/(pow(hot_oven_temp,4) - pow(start_temp,4))/step_precision
    
    current_temp = start_temp
    temp_history = [current_temp]

    while current_temp < end_temp: # basic Euler's Method step-through. 
        next_temp = current_temp + c1*(pow(cold_oven_temp,4) - pow(current_temp,4))
        temp_history.append(next_temp)
        current_temp = next_temp
    
    interp = (end_temp - temp_history[-1])/(temp_history[-2] - temp_history[-1])
    steps = (len(temp_history) - 1) - interp

    time_total = steps*original_time/step_precision
    return time_total
    
# Celcius/Fahrenheit to Kelvin
def temp_convert(temp, type):
    if (type == "C"):
        return (temp + 273.15)
    elif(type == "F"):
        return ((temp - 32) * 5.0/9 + 237.15)
    else:
        print("Invalid Temperature Type. Terminating Program.")
        exit()

# Kelvin to Celcius/Fahrenheit
def temp_uncovert(temp, type):
    if (type == "C"):
        return (temp - 273.15)
    else:
        return ((temp - 273.15) * 9/5 + 32)


print("Welcome to a guide to alternative cooking times.")
print("========================================")
print("Standard Initial Temperatures:")
print("Frozen:              -15°C  or   5°F")
print("Refridgerator:         4°C  or  40°F")
print("Room Temperature:     20°C  or  70°F")
print("========================================")
print("Safe Internal Final Temperatures:")
print("Ground Meat:          75°C  or  165°F")
print("Chicken:              75°C  or  165°F")
print("Pork and Ham:         65°C  or  145°F")
print("Beef / Veal / Lamb:   65°C  or  145°F")
print("Source: https://www.foodsafety.gov/food-safety-charts/safe-minimum-cooking-temperature")
print("========================================")
print("Enter the following values: ")

temp_type   = input('Select Celcius [c] or Fahrenheit [f] run mode: ').upper()

temp_init   = temp_convert(float(input('Intial temp of the food [°' + temp_type + ']: ')), temp_type)
# The initial temperature of the food. 

temp_final  = temp_convert(float(input('Final temp of the food [°' + temp_type + ']: ')), temp_type)
# The final temperature of the food when it's done in the oven.

oven_rec    = temp_convert(float(input('Recommended cooking temp for the food [°' + temp_type + ']: ')), temp_type)
# The recommended cooking temperature

time_rec    = float(input('Recommended cooking time @ previous temp [minutes]: '))
# The recommended cooking time @ the recommended cooking temperature

oven_new    = temp_convert(float(input('At what temp would you like to cook the food instead [°' + temp_type + ']: ')), temp_type)
# The new temperature that you want to cook the food at


print("Now calculating new cooking times...")
new_time = calculate_cook_time(temp_init, temp_final, oven_rec, oven_new, time_rec)
if (new_time < 1): # for extreme examples like surface of sun.
    print("Cook time at alternate temperature: " + str(new_time*60) + " seconds.")
else:
    print("Cook time at alternate temperature: %02d mins." % new_time)


## Now let's loop through and plot a curve. 
low             = temp_convert(100, temp_type)
high            = temp_convert(500, temp_type)
temp_interval   = 5

temp_list = np.array([])
time_list = np.array([])

if low < temp_final: # Error catch.
    low = temp_final + temp_interval

for temp in range(int(low), int(high), temp_interval):
    tmp_time = calculate_cook_time(temp_init, temp_final, oven_rec, temp, time_rec)
    temp_list = np.append(temp_list, temp)
    time_list = np.append(time_list, tmp_time)

temp_list = [temp_uncovert(x, temp_type) for x in temp_list]

fig = plt.figure()
plt.plot(temp_list, time_list, 'ro-', markersize=3)
plt.xlabel("Oven Temperature [°" + temp_type + "]")
plt.ylabel("Equivalent Cooking Time [minutes]")
plt.title("Alternative Cooking Times")
plt.grid()
plt.show()