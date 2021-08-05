# Imports
from re import A
import keyboard  # using module keyboard
import numpy as np
from datetime import datetime
import os

# Variables
a_pitch = 0
a_roll = 0
a_yaw = 0

a_airspeed_indicated = 0
a_alt = 0
a_hdg = 0

a_alpha = 0
a_beta = 0

a_cl = 0
a_cd = 0
a_dynp = 0
a_air_density = 1.3
a_airspeed_true = 50

a_lift_force = 0
a_drag_force = 0

a_lift_vector = np.array([0, 0, 0])
a_drag_vector = np.array([0, 0, 0])
a_thrust_vector = np.array([0, 0 ,0])
a_weight_vector = np.array([0, 0, 0])
a_total_vector = np.array([0, 0, 0])

w_total_vector = np.array([0, 0, 0])

a_elevator_pct = 0
a_aileron_pct = 0
a_rudder_pct = 0

c_wing_area = 50
c_elevator_area = 0
c_aileron_area = 0


# Main loop
while True:  # making a loop
    
    then = datetime.now()        # Random date in the past
    now  = datetime.now()                         # Now
    delta_time = (now - then).total_seconds()      # Total number of seconds between now and then
    #print(delta_time)

    a_lift_force = (0.5 * a_air_density * a_airspeed_true * a_airspeed_true * c_wing_area * a_cl)
    a_cl = -0.007 * (a_alpha - 15) * (a_alpha - 15) + 1.7
    a_lift_vector = ([0, a_lift_force, 0])
    a_total_vector = np.sum([a_lift_vector + a_drag_vector + a_thrust_vector + a_weight_vector], 0)

    print('Alpha:', round(a_alpha))
    print('Roll:', round(a_roll))
    print(a_total_vector)
    print(a_lift_force)
    print(a_cl)
    os.system('cls' if os.name == 'nt' else 'clear')

    
    #add control code here
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):  # if key 'w' is pressed 
            a_alpha = a_alpha - 1
            #print('You Pressed A Key!')
            #break  # finishing the loop

        if keyboard.is_pressed('a'):  # if key 'a' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_roll = a_roll - 1
            
        if keyboard.is_pressed('s'):  # if key 's' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_alpha = a_alpha + 1

        if keyboard.is_pressed('d'):  # if key 'd' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_roll = a_roll + 1

    except:
        break  # if user pressed a key other than the given key the loop will break

