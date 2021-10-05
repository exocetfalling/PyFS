# Imports

import math
from typing import cast
import pygame
import pygame.freetype  # Import the freetype module.

# Variables

# Axes are defined as:
# For aircraft:
# X: left -ve, right +ve
# Y: aft -ve, forward +ve
# Z: down -ve, up +ve

a_vec_linear_accel = [0, 0, 0]
a_vec_linear_velocity = [0, 0, 0]
a_mag_linear_velocity = 0

a_vec_angular_accel = [0, 0, 0]
a_vec_angular_vel = [0, 0, 0]
a_alpha = 0
a_beta = 0
a_wing_cl = 0

a_fpa = 0
a_trk = 0

# For world:
# X: west -ve, east +ve
# Y: south -ve, north +ve
# Z: down -ve, up +ve

w_vec_linear_accel = [0, 0, 0]
w_vec_linear_velocity = [0, 0, 0]
w_mag_linear_velocity = 0
w_vec_linear_dis = [0, 0, 0]

w_vec_angular_accel = [0, 0, 0]
w_vec_angular_vel = [0, 0, 0]

# [pitch, roll, heading]
w_vec_angular_dis = [0, 0, 0]

# Controls
a_elevator_angle_rad = 0
a_aileron_angle_rad = 0
a_rudder_angle_rad = 0

# Lengths in m
c_dimensions_aircraft_length = 10
c_dimensions_aircraft_width = 20
c_dimensions_aircraft_height = 4

c_wing_incidence = math.pi/60

c_position_tailplane_horizontal = -9
c_position_tailplane_vertical = -9
c_position_wing = 0
c_position_elevator = -10
c_position_aileron_left = -18
c_position_aileron_right = 18
c_position_rudder = -10

# Areas in m^2
c_area_wing = 30
c_area_tailplane_horizontal = 2
c_area_tailplane_vertical = 2
c_area_aileron = 0.5
c_area_elevator = 0.5
c_area_rudder = 0.5

c_area_rot_drag = [40, 40, 30]

# Masses in kg
c_mass_aircraft = 1000

# MOIs in kg m^2
# Using formula:
# MOI = 1/12 * mass * (length)^2
c_moi = [8333, 33333, 8333]


pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 60
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Functions
def Convert_Vec_Frame_Acft_To_World(vec_a_frame, angle_fpa, angle_trk): 
    vec_rot_fpa = [vec_a_frame[0], vec_a_frame[1] * math.cos(angle_fpa), vec_a_frame[2] * math.sin(angle_fpa)]
    vec_rot_trk = [vec_rot_fpa[0] * math.sin(angle_trk), vec_rot_fpa[1] * math.cos(angle_trk), vec_rot_fpa[2]]
    return vec_rot_trk

def Convert_Vec_Gravity_Acc_World_To_Acft(angle_pitch, angle_roll): 
    vec_gravity_world = [0, 0, -9.8065]
    vec_gravity_rot_pitch = [0, vec_gravity_world[2] * math.sin(angle_pitch), vec_gravity_world[2] * math.cos(angle_pitch)]
    vec_gravity_rot_roll = [vec_gravity_rot_pitch[2] * math.sin(-angle_roll), vec_gravity_rot_pitch[1], vec_gravity_rot_pitch[2] * math.cos(angle_roll)]
    return vec_gravity_rot_roll

def Calc_Force_Angular_Acc(axis_moi, force_magnitude, distance_from_pivot):
    return force_magnitude * distance_from_pivot / axis_moi

def Calc_Vec_Mag(vec_input):
    mag_vec = math.sqrt(pow(vec_input[0], 2) + pow(vec_input[1], 2) + pow(vec_input[2], 2))
    return mag_vec

def Calc_Force_Acc(force_magnitude, mass_kg):
    return force_magnitude / mass_kg

def Limit_Angle(angle_rad, angle_min, angle_max):
    if (angle_rad < angle_min):
        return angle_rad + 2*math.pi
    elif (angle_rad > angle_max):
        return angle_rad - 2*math.pi
    else:
        return angle_rad

def Calc_Integral_Scalar(value, time_interval):
    return value * time_interval

def Calc_Airflow_Angle(vel_side, vel_total_mag):
    if (vel_total_mag != 0):
        return -math.asin(vel_side / vel_total_mag)
    else:
        return 0

def Calc_Lift_Coeff(angle_alpha_rad):
    
    x1 = -math.pi
    y1 = 0
    x2 = -math.pi/12
    y2 = -1.5
    x3 = math.pi/12
    y3 = 1.5
    x4 = math.pi
    y4 = 0

    a = (y2 - y1) / (x2 - x1)
    b = (y3 - y2) / (x3 - x2)
    c = (y4 - y3) / (x4 - x3)

    if ((angle_alpha_rad > x1) and (angle_alpha_rad <= x2)):
        return (a * (angle_alpha_rad - x1) + y1)
    
    elif ((angle_alpha_rad > x2) and (angle_alpha_rad <= x3)):
        return (b * (angle_alpha_rad - x2) + y2)

    elif ((angle_alpha_rad > x3) and (angle_alpha_rad <= x4)):
        return (c * (angle_alpha_rad - x3) + y3)

    else:
        raise NameError('CalcCLErr')

def Calc_Integral_Vector(vec_current, vec_derivative, time_interval):
    vec_output = [0, 0, 0]

    vec_output[0] = vec_current[0] + vec_derivative[0] * time_interval
    vec_output[1] = vec_current[1] + vec_derivative[1] * time_interval
    vec_output[2] = vec_current[2] + vec_derivative[2] * time_interval

    return vec_output

def Calc_Drag_Coeff(angle_rad):
    return 0.05 * math.sin(angle_rad)

def Calc_Force_Lift(air_density, airspeed_true, surface_area, lift_coeff):
    return 0.5 * air_density * math.pow(airspeed_true, 2) * surface_area * lift_coeff

def Calc_Force_Drag(air_density, airspeed_true, surface_area, drag_coeff):
    return -0.5 * air_density * airspeed_true * airspeed_true * surface_area * drag_coeff

def Calc_Drag_Angular(air_density, velocity_rotational, surface_area):
    return -air_density * velocity_rotational * surface_area
    #return -0.5 * air_density * pow(velocity_rotational, 2) * surface_area

def Convert_Angle_Rad_To_Deg(angle_rad):
    return angle_rad * 57.2958

def Convert_Angle_Deg_To_Rad(angle_deg):
    return angle_deg / 57.2958

def blit_text(surface, text, pos, font, color=pygame.Color('green')):
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

    a_alpha = Calc_Airflow_Angle(a_vec_linear_velocity[2], a_mag_linear_velocity)
    a_beta = Calc_Airflow_Angle(a_vec_linear_velocity[0], a_mag_linear_velocity)

    a_fpa = w_vec_angular_dis[0] - a_alpha
    a_trk = w_vec_angular_dis[2] - a_beta

    a_wing_cl = Calc_Lift_Coeff(a_alpha)

    w_vec_angular_dis[0] = Limit_Angle(w_vec_angular_dis[0], -math.pi, +math.pi)
    w_vec_angular_dis[1] = Limit_Angle(w_vec_angular_dis[1], -math.pi, +math.pi)
    w_vec_angular_dis[2] = Limit_Angle(w_vec_angular_dis[2], 0, +2*math.pi)

    a_vec_linear_accel = Convert_Vec_Gravity_Acc_World_To_Acft(w_vec_angular_dis[0], w_vec_angular_dis[1])
    a_vec_linear_velocity = Calc_Integral_Vector(a_vec_linear_velocity, a_vec_linear_accel, dt)
    a_mag_linear_velocity = Calc_Vec_Mag(a_vec_linear_velocity)
    w_vec_linear_accel = Convert_Vec_Frame_Acft_To_World(a_vec_linear_accel, a_fpa, a_trk)
    w_vec_linear_velocity = Calc_Integral_Vector(w_vec_linear_velocity, w_vec_linear_accel, dt)
    w_mag_linear_velocity = Calc_Vec_Mag(w_vec_linear_velocity)
    w_vec_linear_dis = Calc_Integral_Vector(w_vec_linear_dis, w_vec_linear_velocity, dt)


    debug_text = \
        '\nACFT:'            + \
        '\nX Vel: '        + str(round(a_vec_linear_velocity[0], 2)) + \
        '\nY Vel: '        + str(round(a_vec_linear_velocity[1], 2)) + \
        '\nZ Vel: '        + str(round(a_vec_linear_velocity[2], 2)) + \
        '\nX Acc: '        + str(round(a_vec_linear_accel[0], 2)) + \
        '\nY Acc: '        + str(round(a_vec_linear_accel[1], 2)) + \
        '\nZ Acc: '        + str(round(a_vec_linear_accel[2], 2)) + \
        '\nPITCH ACCEL: '  + str(round(a_vec_angular_accel[0], 2)) + \
        '\nPITCH VEL: '    + str(round(a_vec_angular_vel[0], 2)) + \
        '\nALPHA: '        + str(round(Convert_Angle_Rad_To_Deg(a_alpha), 2)) + \
        '\nCL: '           + str(round(a_wing_cl, 2)) + \
        '\nWORLD:'         + \
        '\nX Vel: '        + str(round(w_vec_linear_velocity[0], 2)) + \
        '\nY Vel: '        + str(round(w_vec_linear_velocity[1], 2)) + \
        '\nZ Vel: '        + str(round(w_vec_linear_velocity[2], 2)) + \
        '\nX Acc: '        + str(round(w_vec_linear_accel[0], 2)) + \
        '\nY Acc: '        + str(round(w_vec_linear_accel[1], 2)) + \
        '\nZ Acc: '        + str(round(w_vec_linear_accel[2], 2)) + \
        '\nPITCH: '        + str(round((w_vec_angular_dis[0]), 2)) + \
        '\nFPA: '          + str(round(Convert_Angle_Rad_To_Deg(a_fpa), 2)) + \
        '\nROLL: '         + str(round(Convert_Angle_Rad_To_Deg(w_vec_angular_dis[1]), 2)) + \
        '\nHDG: '          + str(round(Convert_Angle_Rad_To_Deg(w_vec_angular_dis[2]), 2))

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        w_vec_angular_dis[0] = w_vec_angular_dis[0] - math.pi/180

    if keys[pygame.K_s]:
        w_vec_angular_dis[0] = w_vec_angular_dis[0] + math.pi/180

    if keys[pygame.K_a]:
        w_vec_angular_dis[1] = w_vec_angular_dis[1] - math.pi/180

    if keys[pygame.K_d]:
        w_vec_angular_dis[1] = w_vec_angular_dis[1] + math.pi/180

    if keys[pygame.K_q]:
        w_vec_angular_dis[2] = w_vec_angular_dis[2] - math.pi/180

    if keys[pygame.K_e]:
        w_vec_angular_dis[2] = w_vec_angular_dis[2] + math.pi/180


    if keys[pygame.K_r]:
        w_vec_angular_dis = [0, 0, 0]


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('black'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()
