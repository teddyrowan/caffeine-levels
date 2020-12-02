"""
# Coffee example. Uniform over 20 mins. Change intensity to 5mg/step instead of 100mg/step
pill_time = np.array([])
for ii in range(0, 20): #morning coffee
    pill_time = np.append(pill_time, ii)
for ii in range(210, 230): #noon coffee
    pill_time = np.append(pill_time, ii)
for ii in range(450, 470): #4pm coffee
    pill_time = np.append(pill_time, ii)
pill_time = pill_time + time_delay
"""