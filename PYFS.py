# Imports
import keyboard  # using module keyboard
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
a_air_density = 0
a_airspeed_true = 0

a_lift_force = 0
a_drag_force = 0

a_lift_vector = [0, 0, 0]
a_drag_vector = [0, 0, 0]
a_thrust_vector = [0, 0 ,0]
a_total_vector = [0, 0, 0]

w_weight_vector = [0, 0, 0]
w_total_vector = [0, 0, 0]

a_elevator_pct = 0
a_aileron_pct = 0
a_rudder_pct = 0

c_wing_area = 0
c_elevator_area = 0
c_aileron_area = 0

# Functions

def calc_lift_force(a_air_density, a_airspeed_true, c_wing_area, a_cl):
    a_lift_force = (0.5 * a_air_density * a_airspeed_true * a_airspeed_true * c_wing_area * a_cl)
    return a_lift_force

def calc_cl(a_alpha):
    a_cl = -0.007 * (a_alpha - 15) * (a_alpha - 15) + 1.7
    return a_cl

def calc_lift_vector(a_lift_force):
    a_lift_vector = [0, a_lift_force, 0]
    return a_lift_vector

# Main loop
while True:  # making a loop
    
    then = datetime.now()        # Random date in the past
    now  = datetime.now()                         # Now
    delta_time = (now - then).total_seconds()      # Total number of seconds between now and then
    #print(delta_time)
    print('Pitch:', round(a_pitch))
    print('Roll:', round(a_roll))
    os.system('cls' if os.name == 'nt' else 'clear')

    
    #add control code here
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):  # if key 'w' is pressed 
            a_pitch = a_pitch - 1
            #print('You Pressed A Key!')
            #break  # finishing the loop

        if keyboard.is_pressed('a'):  # if key 'a' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_roll = a_roll - 1
            
        if keyboard.is_pressed('s'):  # if key 's' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_pitch = a_pitch + 1

        if keyboard.is_pressed('d'):  # if key 'd' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_roll = a_roll + 1

    except:
        break  # if user pressed a key other than the given key the loop will break

