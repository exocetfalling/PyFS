# Imports
from re import A
import keyboard  # using module keyboard
import numpy as np
import math
from datetime import datetime
import os
import pygame
import pygame.freetype  # Import the freetype module.

# Variables
a_fpa_deg = 0
a_fpa_rad = 0
a_roll_deg = 0
a_roll_rad = 0

a_airspeed_indicated = 0
a_alt = 0
a_trk_rad = 0
a_trk_deg = 0

a_alpha = 0
a_beta = 0

a_cl = 0
a_cd = 0
a_dynp = 0
a_air_density = 1.3
a_airspeed_true = 50
a_gnd_speed = 50
a_lift_force = 0
a_drag_force = 0

w_x_velocity = 0
w_y_velocity = 0
w_z_velocity = 0

w_x_pos = 0
w_y_pos = 0
w_z_pos = 0

""" 
a_lift_vector = np.array([0, 0, 0])
a_drag_vector = np.array([0, 0, 0])
a_thrust_vector = np.array([0, 0 ,0])
a_weight_vector = np.array([0, 0, 0])
a_total_vector = np.array([0, 0, 0])

w_total_vector = np.array([0, 0, 0])
 """

a_elevator_pct = 0
a_aileron_pct = 0
a_rudder_pct = 0

c_wing_area = 50
c_elevator_area = 0
c_aileron_area = 0

s_fps = 0
s_counter = 0

pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 30
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Functions
def Calc_Velocity_World(axis, total_vel, angle_horizontal, angle_vertical): 
    if axis == 'x':
        return (total_vel * math.sin(angle_horizontal)) * math.cos(angle_vertical)
    if axis == 'y':
        return (total_vel * math.cos(angle_horizontal)) * math.cos(angle_vertical)
    if axis == 'z':
        return (total_vel * math.sin(angle_vertical)) * math.cos(angle_horizontal)

def Calc_Force_Moment(force_magnitude, distance_from_pivot):
    return force_magnitude * distance_from_pivot

def Calc_Force_Acc(force_magnitude, mass_kg):
    return force_magnitude / mass_kg

def Calc_Lift_Coeff(angle_rad):
    return -0.007 * (angle_rad - 15) * (angle_rad - 15) + 1.7

def Calc_Drag_Coeff(angle_rad):
    return math.sin(angle_rad)

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.



font = pygame.font.SysFont('Courier', 16)

while True:

    dt = clock.tick(FPS) / 1000
    debug_text = \
        '\nX Pos: ' + str(w_x_pos) + \
        '\nY Pos: ' + str(w_y_pos) + \
        '\nZ Pos: ' + str(w_z_pos) + \
        '\nFPA: ' + str(a_fpa_deg) + \
        '\nHDG: ' + str(a_trk_deg)
    a_trk_deg = (a_trk_deg + 360) % 360
    a_fpa_deg = (a_fpa_deg + 180) % 180
    a_trk_rad = a_trk_deg / 57.2958
    a_fpa_rad = a_fpa_deg / 57.2958
    a_lift_force = (0.5 * a_air_density * a_airspeed_true * a_airspeed_true * c_wing_area * a_cl)
    a_cl = Calc_Lift_Coeff(a_alpha)
    
    """     
    w_x_velocity = (a_gnd_speed * math.sin(a_hdg_rad)) * math.cos(a_fpa_rad)
    w_y_velocity = (a_gnd_speed * math.cos(a_hdg_rad)) * math.cos(a_fpa_rad)
    w_z_velocity = a_gnd_speed * math.sin(a_fpa_rad)

    """
    w_x_velocity = Calc_Velocity_World('x', a_gnd_speed, a_trk_rad, a_fpa_rad)
    w_y_velocity = Calc_Velocity_World('y', a_gnd_speed, a_trk_rad, a_fpa_rad)
    w_z_velocity = Calc_Velocity_World('z', a_gnd_speed, a_roll_rad, a_fpa_rad)

    w_x_pos = w_x_pos + w_x_velocity * dt
    w_y_pos = w_y_pos + w_y_velocity * dt
    w_z_pos = w_z_pos + w_z_velocity * dt

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        a_fpa_deg = a_fpa_deg - 10 * dt

    if keys[pygame.K_s]:
        a_fpa_deg = a_fpa_deg + 10 * dt

    if keys[pygame.K_a]:
        a_trk_deg = a_trk_deg - 10 * dt

    if keys[pygame.K_d]:
        a_trk_deg = a_trk_deg + 10 * dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('white'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()

# Main loop
while True:  # making a loop
    
    then = datetime.now()        # Random date in the past
    now  = datetime.now()                         # Now
    dt = (now - then).total_seconds()      # Total number of seconds between now and then
    #print(dt)
    
    s_counter = s_counter + 1

    os.system('cls' if os.name == 'nt' else 'clear')

    print('Pitch:', round(a_fpa_deg))
    print('Heading:', round(a_hdg_deg))
    print('X Vel:', round(w_x_velocity))
    print('Y Vel:', round(w_y_velocity))
    print('Z Vel:', round(w_z_velocity))
    print('X Pos:', round(w_x_pos))
    print('Y Pos:', round(w_y_pos))
    print('Z Pos:', round(w_z_pos))
    print('Delta Time:', dt)




    """     
    a_lift_vector = ([0, a_lift_force, 0])
    a_total_vector = np.sum([a_lift_vector + a_drag_vector + a_thrust_vector + a_weight_vector], 0)
    """
    

    """ 
    print(a_total_vector)
    print(a_lift_force)
    print(a_cl)

    """


    
    #add control code here
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):  # if key 'w' is pressed 
            a_fpa_deg = a_fpa_deg - 0.1
            #print('You Pressed A Key!')
            #break  # finishing the loop

        if keyboard.is_pressed('a'):  # if key 'a' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_roll = a_roll - 0.1
            
        if keyboard.is_pressed('s'):  # if key 's' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_fpa_deg = a_fpa_deg + 0.1

        if keyboard.is_pressed('d'):  # if key 'd' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_roll = a_roll + 0.1

        if keyboard.is_pressed('e'):  # if key 'd' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_hdg_deg = a_hdg_deg + 0.1

        if keyboard.is_pressed('q'):  # if key 'd' is pressed 
            #print('You Pressed A Key!')
            #break  # finishing the loop
            a_hdg_deg = a_hdg_deg - 0.1

    

    except:
        break  # if user pressed a key other than the given key the loop will break

