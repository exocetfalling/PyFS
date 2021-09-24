# Imports

import math
from typing import cast
import pygame
import pygame.freetype  # Import the freetype module.

# Variables

# Polar coordinates as as commonly used in physics (ISO 80000-2:2019 convention): 
# radial distance r (distance to origin), 
# polar angle theta (angle with respect to polar axis), 
# azimuthal angle phi (angle of rotation from the initial meridian plane).

a_theta_deg = 0
a_theta_rad = 0
a_phi_deg = 90
a_phi_rad = math.pi/2
a_radial_velocity = 50

a_accel_x = 0
a_accel_y = 0
a_accel_z = 0

a_x_velocity = 0
a_y_velocity = 50
a_z_velocity = 0

a_total_velocity = 50

a_angular_accel_x = 0
a_angular_accel_y = 0
a_angular_accel_z = 0

a_angular_vel_x = 0
a_angular_vel_y = 0
a_angular_vel_z = 0

a_angular_displacement_x = 0
a_angular_displacement_y = 0
a_angular_displacement_z = 0

a_airspeed_indicated = 0
a_alt = 0

a_pitch_rad = 0
a_roll_rad = 0

a_alpha_rad = 0
a_beta_rad = 0

a_fpa_rad = 0
a_hdg_rad = 0
a_trk_rad = 0

a_cl_wing = 0
a_cl_tailplane_horizontal = 0
a_cl_tailplane_vertical = 0

a_cl_elevator = 0
a_cl_aileron_left = 0
a_cl_aileron_right = 0
a_cl_rudder = 0

a_cd_wing = 0
a_dynp = 0
a_air_density = 1.3
a_airspeed_true = 50

a_lift_force_elevator = 0
a_lift_force_aileron_left = 0
a_lift_force_aileron_right = 0
a_lift_force_rudder = 0

a_lift_force_wing = 0
a_lift_force_tailplane_horizontal = 0
a_lift_force_tailplane_vertical = 0

a_drag_force_wing = 0

a_angular_damping_x = 0

a_thrust_force = 0

# Axes are defined as:
# For aircraft:
# X: left -ve, right +ve
# Y: aft -ve, forward +ve
# Z: down -ve, up +ve

# For world:
# X: west -ve, east +ve
# Y: south -ve, north +ve
# Z: down -ve, up +ve

w_x_velocity = 0
w_y_velocity = 0
w_z_velocity = 0

w_vec_velocity = [0, 0, 0]

w_x_pos = 0
w_y_pos = 0
w_z_pos = 0

w_vec_pos = [0, 0, 0]

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

c_area_rot_drag_x = 30
c_area_rot_drag_y = 20
c_area_rot_drag_z = 20

# Masses in kg
c_mass_aircraft = 1000

# MOIs in kg m^2
# Using formula:
# MOI = 1/12 * mass * (length)^2
c_moi_pitch = 8333
c_moi_roll = 33333
c_moi_yaw = 8333

a_accel_x_grav = 0
a_accel_y_grav = 0
a_accel_z_grav = 0

pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 60
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Functions
def Calc_Velocity_World(axis, total_vel, angle_azimuthal, angle_polar): 
    if axis == 'x':
        return (total_vel * math.sin(angle_azimuthal)) * math.sin(angle_polar)
    if axis == 'y':
        return (total_vel * math.cos(angle_azimuthal)) * math.sin(angle_polar)
    if axis == 'z':
        return (total_vel * math.cos(angle_azimuthal))

def Calc_Velocity_Total_Magnitude(vel_x, vel_y, vel_z):
    return math.sqrt(math.sqrt((pow(vel_x, 2) + pow(vel_y, 2))) + pow(vel_z, 2))

def Calc_Force_Angular_Acc(axis_moi, force_magnitude, distance_from_pivot):
    return force_magnitude * distance_from_pivot / axis_moi

def Calc_Angular_Vel():
    pass

def Calc_Force_Acc(force_magnitude, mass_kg):
    return force_magnitude / mass_kg

def Calc_Integral(value, time_interval):
    return value * time_interval

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


def Calc_Drag_Coeff(angle_rad):
    return 0.05 * math.sin(angle_rad)

def Calc_Force_Lift(air_density, airspeed_true, surface_area, lift_coeff):
    return 0.5 * air_density * math.pow(airspeed_true, 2) * surface_area * lift_coeff

def Calc_Force_Drag(air_density, airspeed_true, surface_area, drag_coeff):
    return -0.5 * air_density * airspeed_true * airspeed_true * surface_area * drag_coeff

def Calc_Drag_Angular(air_density, velocity_rotational, surface_area, drag_coeff):
    return -0.5 * air_density * pow(velocity_rotational, 2) * surface_area * drag_coeff


def Calc_Acc_Gravity(axis, angle_roll, angle_pitch):
    if (axis == 'x'):
        return -9.8065 * math.sin(angle_roll)
    if (axis == 'y'):
        return -9.8065 * math.sin(angle_pitch)
    if (axis == 'z'):
        return -9.8065 * math.cos(angle_pitch)

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
    debug_text = \
        '\nX Vel: ' + str(round(a_x_velocity, 2)) + \
        '\nY Vel: ' + str(round(a_y_velocity, 2)) + \
        '\nZ Vel: ' + str(round(a_z_velocity, 2)) + \
        '\nTotal: ' + str(round(a_total_velocity, 2)) + \
        '\nPITCH ACCEL: ' + str(round(a_angular_accel_x, 2)) + \
        '\nPITCH VEL: ' + str(round(a_angular_vel_x, 2)) + \
        '\nPITCH: ' + str(round(Convert_Angle_Rad_To_Deg(a_pitch_rad), 2)) + \
        '\nROLL: ' + str(round(Convert_Angle_Rad_To_Deg(a_roll_rad), 2)) + \
        '\nALPHA: ' + str(round(Convert_Angle_Rad_To_Deg(a_alpha_rad), 2))
    a_phi_deg = (a_phi_deg + 360) % 360
    a_theta_deg = (a_theta_deg + 360) % 360

    a_phi_rad = Convert_Angle_Deg_To_Rad(a_phi_deg)
    a_theta_rad = Convert_Angle_Deg_To_Rad(a_theta_deg)

    a_pitch_rad = a_angular_displacement_x * math.cos(a_roll_rad)
    a_roll_rad = a_angular_displacement_y
    
    a_alpha_rad = -math.asin(a_z_velocity / a_total_velocity)
    a_beta_rad = -math.asin(a_x_velocity / a_total_velocity)

    a_fpa_rad = a_pitch_rad - a_alpha_rad
    a_trk_rad = a_hdg_rad - a_beta_rad

    a_lift_force_wing = Calc_Force_Lift(a_air_density, a_airspeed_true, c_area_wing, (Calc_Lift_Coeff(a_alpha_rad + c_wing_incidence)))
    a_lift_force_tailplane_horizontal = Calc_Force_Lift(a_air_density, a_airspeed_true, c_area_tailplane_horizontal, (Calc_Lift_Coeff(a_alpha_rad)))
    a_lift_force_tailplane_vertical = Calc_Force_Lift(a_air_density, a_airspeed_true, c_area_tailplane_vertical, (Calc_Lift_Coeff(a_beta_rad)))
    
    a_drag_force_wing = Calc_Force_Drag(a_air_density, a_airspeed_true, c_area_wing, (Calc_Drag_Coeff(a_alpha_rad + c_wing_incidence)))

    a_airspeed_true = a_total_velocity

    a_accel_x_grav = Calc_Acc_Gravity('x', a_roll_rad, a_pitch_rad)
    a_accel_y_grav = Calc_Acc_Gravity('y', a_roll_rad, a_pitch_rad)
    a_accel_z_grav = Calc_Acc_Gravity('z', a_roll_rad, a_pitch_rad)

    a_accel_x = \
        Calc_Force_Acc(a_lift_force_rudder, c_mass_aircraft) + \
        Calc_Force_Acc(a_lift_force_tailplane_vertical, c_mass_aircraft) + \
        Calc_Acc_Gravity('x', a_roll_rad, a_pitch_rad)
    a_accel_y = \
        Calc_Force_Acc(a_thrust_force, c_mass_aircraft) + \
        Calc_Force_Acc(a_drag_force_wing, c_mass_aircraft) + \
        Calc_Acc_Gravity('y', a_roll_rad, a_pitch_rad)
    a_accel_z = \
        Calc_Force_Acc(a_lift_force_wing, c_mass_aircraft) + \
        Calc_Force_Acc(a_lift_force_elevator, c_mass_aircraft) + \
        Calc_Acc_Gravity('z', a_roll_rad, a_pitch_rad)

    a_x_velocity = a_x_velocity + Calc_Integral(a_accel_x, dt)
    a_y_velocity = a_y_velocity + Calc_Integral(a_accel_y, dt)
    a_z_velocity = a_z_velocity + Calc_Integral(a_accel_z, dt)

    # a_total_velocity = Calc_Velocity_Total_Magnitude(a_x_velocity, a_y_velocity, a_z_velocity)
    a_total_velocity = math.hypot(a_x_velocity, a_y_velocity, a_z_velocity)
    

    a_angular_accel_x = \
        Calc_Force_Angular_Acc(c_moi_pitch, a_lift_force_tailplane_horizontal, c_position_tailplane_horizontal) + \
        Calc_Force_Angular_Acc(c_moi_pitch, a_lift_force_elevator, c_position_elevator) + \
        Calc_Force_Angular_Acc(c_moi_pitch, a_lift_force_wing, c_position_wing) + \
        -16 * a_angular_vel_x
    a_angular_accel_y = \
        Calc_Force_Angular_Acc(c_moi_roll, a_lift_force_aileron_left, c_position_aileron_left) + \
        Calc_Force_Angular_Acc(c_moi_roll, a_lift_force_aileron_right, c_position_aileron_right) + \
        -8 * a_angular_vel_y
    a_angular_accel_z = \
        Calc_Force_Angular_Acc(c_moi_yaw, a_lift_force_tailplane_vertical, c_position_tailplane_vertical) + \
        Calc_Force_Angular_Acc(c_moi_yaw, a_lift_force_rudder, c_position_rudder)

    a_angular_vel_x = a_angular_vel_x + Calc_Integral(a_angular_accel_x, dt)
    a_angular_vel_y = a_angular_vel_y + Calc_Integral(a_angular_accel_y, dt)
    a_angular_vel_z = a_angular_vel_z + Calc_Integral(a_angular_accel_z, dt)

    a_angular_displacement_x = a_angular_displacement_x + Calc_Integral(a_angular_vel_x, dt)
    a_angular_displacement_y = a_angular_displacement_y + Calc_Integral(a_angular_vel_y, dt)
    a_angular_displacement_z = a_angular_displacement_z + Calc_Integral(a_angular_vel_z, dt)

    # a_angular_displacement_x = ((a_angular_displacement_x + (2 * math.pi)) % (2 * math.pi)) - (math.pi)

    w_x_velocity = Calc_Velocity_World('x', a_total_velocity, a_phi_rad, a_theta_rad)
    w_y_velocity = Calc_Velocity_World('y', a_total_velocity, a_phi_rad, a_theta_rad)
    w_z_velocity = Calc_Velocity_World('z', a_total_velocity, a_roll_rad, a_theta_rad)

    w_vec_velocity = [w_x_velocity, w_y_velocity, w_z_velocity]

    w_x_pos = w_x_pos + w_x_velocity * dt
    w_y_pos = w_y_pos + w_y_velocity * dt
    w_z_pos = w_z_pos + w_z_velocity * dt

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        a_angular_vel_x = -math.pi/30

    if keys[pygame.K_s]:
        a_angular_vel_x =  math.pi/30

    if keys[pygame.K_a]:
        a_angular_vel_y = -math.pi/30

    if keys[pygame.K_d]:
        a_angular_vel_y =  math.pi/30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('black'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()
