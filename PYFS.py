import keyboard  # using module keyboard
from datetime import datetime
import os

a_pitch = 0
a_roll = 0
a_yaw = 0

a_spd = 0
a_alt = 0
a_hdg = 0

a_alpha = 0
a_beta = 0

a_elevator_pct = 0
a_aileron_pct = 0
a_rudder_pct = 0



while True:  # making a loop
    
    then = datetime.now()        # Random date in the past
    now  = datetime.now()                         # Now
    delta_time = (now - then).total_seconds()      # Total number of microseconds between dates
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
